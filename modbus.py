import pymodbus.client as ModbusClient
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "G_WAOJWZ1ymjZLUn9L1ZsrpKxYIsUYk42g7AARJgc3CdIT5GEdzLOn9gdT2MYVvIL1k46o_4QV3OQ9KgfP3txQ=="
influxdb_address = 'pdu_poll-influxdb-1:8096'
org='byu'
bucket = 'pdu-data'
url = f"http://{influxdb_address}"

influx_client = influxdb_client.InfluxDBClient(url=url,token=token,org=org)

pdu_ips = [{'ip': '10.11.82.11', 'name': '1400N_100E_B'}]#, {'ip': '10.11.82.12', 'name': '1400N 100E C'}, {'ip': '10.11.82.13', 'name': '1400N 200E B'},
#            {'ip': '10.11.82.14', 'name': '1400N 200E C'}, {'ip': '10.11.82.15', 'name': '1400N 300E B'}, {'ip': '10.11.82.16', 'name': '1400N 300E C'},
#            {'ip': '10.11.82.17', 'name': '1400N 400E B'}, {'ip': '10.11.82.18', 'name': '1400N 400E C'}, {'ip': '10.11.82.19', 'name': '1400N 500E B'},
#            {'ip': '10.11.82.20', 'name': '1400N 500E C'}, {'ip': '10.11.82.21', 'name': '1400N 600E B'}, {'ip': '10.11.82.22', 'name': '1400N 600E C'},
#            {'ip': '10.11.82.23', 'name': '1400N 700E B'},{'ip': '10.11.82.24', 'name': '1400N 700E C'}]

pdu_registers = [{'register': 299, 'mapping': 'Total Real Power', 'units': 'watts'},
                 {'register': 300, 'mapping': 'Total Apparent Power', 'units': 'volt-amps'},
                 {'register': 301, 'mapping': 'Total Power Factor', 'units': '%'},
                 {'register': 302, 'mapping': 'Total Energy', 'units': 'kilowatt-hours'}
                 ]
device_ip = '10.11.82.24'
device_port = 502


# try:
#     client = ModbusClient.ModbusTcpClient(device_ip, port=device_port, timeout = 10)
#     connection = client.connect()

#     if connection:
#         print('connected')
#         print(connection)
#         response = client.read_holding_registers(409, 1, unit=1)
       
#         if response.isError():
#             print(f"Modbus error")
#             print(response)
#         else:
#             print(response.registers[0]/100)

#     client.close()
#     print('client closed')
# except Exception as e:
#     print(f"Error: {e}")


for pdu in pdu_ips:
    try:
        data = []
        client = ModbusClient.ModbusTcpClient(pdu['ip'], port=device_port,timeout=10)
        connection = client.connect()

        if connection:
            for reading in pdu_registers:
                response=client.read_holding_registers(reading['register'],1,unit=1)
                if response.isError():
                    print(f"Modbus Error")
                else:
                    data.append({'value': response.registers[0], 'mapping': reading['mapping'], 'units': reading['units']})
        client.close()
        print(data)
        write_api = influx_client.write_api(write_options=SYNCHRONOUS)
        for point_value in data:
            point = (
                Point(point_value['mapping'])
                .tag('pdu_name', pdu['name'])
                .field(point_value['units'], point_value['value'])
            )
            write_api.write(bucket=bucket,org='byu',record=point)

    except Exception as e:
        print(f"Error:{e}")
