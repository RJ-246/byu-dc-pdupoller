import pymodbus.client as ModbusClient
import influxdb_client, os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#Sets up influxDB info
token = os.environ['INFLUX_TOKEN']
influxdb_address = 'pdu-poll-influxdb-1:8086'
org='byu'
bucket = 'pdu-data'
url = f"http://{influxdb_address}"

influx_client = influxdb_client.InfluxDBClient(url=url,token=token,org=org)

#All IPs for PDUs
pdu_ips = [{'ip': '10.11.82.11', 'name': '1400N 100E B'}, {'ip': '10.11.82.12', 'name': '1400N 100E C'}, {'ip': '10.11.82.13', 'name': '1400N 200E B'},
           {'ip': '10.11.82.14', 'name': '1400N 200E C'}, {'ip': '10.11.82.15', 'name': '1400N 300E B'}, {'ip': '10.11.82.16', 'name': '1400N 300E C'},
           {'ip': '10.11.82.17', 'name': '1400N 400E B'}, {'ip': '10.11.82.18', 'name': '1400N 400E C'}, {'ip': '10.11.82.19', 'name': '1400N 500E B'},
           {'ip': '10.11.82.20', 'name': '1400N 500E C'}, {'ip': '10.11.82.21', 'name': '1400N 600E B'}, {'ip': '10.11.82.22', 'name': '1400N 600E C'},
           {'ip': '10.11.82.23', 'name': '1400N 700E B'},{'ip': '10.11.82.24', 'name': '1400N 700E C'},
           
           {'ip': '10.11.82.25', 'name': '900N 100E A'}, {'ip': '10.11.82.26', 'name': '900N 100E B'}, {'ip':'10.11.82.27', 'name': '900N 200E A'},
           {'ip': '10.11.82.28' ,'name': '900N 200E B'}, {'ip': '10.11.82.29','name': '900N 300E A'}, {'ip': '10.11.92.30','name': '900N 300E B'},
           {'ip': '10.11.82.31','name': '900N 400E A'}, {'ip': '10.11.82.32','name':'900N 400E B'}, {'ip': '10.11.82.33','name':'900N 500E A'},
           {'ip': '10.11.82.34','name':'900N 500E B'}, {'ip': '10.11.82.35','name':'900N 600E B'}, {'ip': '10.11.82.36','name':'900N 600E C'},
           {'ip': '10.11.82.37','name':'900N 700E A'}, {'ip': '10.11.82.38','name':'900N 700E B'}]

#The registers to read data from (each pdu has a CSV you can download with the register mappings)
pdu_registers = [{'register': 299, 'mapping': 'Total Real Power', 'units': 'watts'},
                 {'register': 300, 'mapping': 'Total Apparent Power', 'units': 'volt-amps'},
                 {'register': 301, 'mapping': 'Total Power Factor', 'units': '%'},
                 {'register': 302, 'mapping': 'Total Energy', 'units': 'kilowatt-hours'},

                 {'register': 400, 'mapping': 'Phase 1 Voltage', 'units': 'volts'},
                 {'register': 401, 'mapping': 'Phase 2 Voltage', 'units': 'volts'},
                 {'register': 402, 'mapping': 'Phase 3 Voltage', 'units': 'volts'},
                 {'register': 403, 'mapping': 'Phase 4 Voltage', 'units': 'volts'},
                 {'register': 404, 'mapping': 'Phase 5 Voltage', 'units': 'volts'},
                 {'register': 405, 'mapping': 'Phase 6 Voltage', 'units': 'volts'},

                 {'register': 410, 'mapping': 'Phase 1 Current', 'units': 'amps'},
                 {'register': 411, 'mapping': 'Phase 2 Current', 'units': 'amps'},
                 {'register': 412, 'mapping': 'Phase 3 Current', 'units': 'amps'},
                 {'register': 413, 'mapping': 'Phase 4 Current', 'units': 'amps'},
                 {'register': 414, 'mapping': 'Phase 5 Current', 'units': 'amps'},
                 {'register': 415, 'mapping': 'Phase 6 Current', 'units': 'amps'},

                 {'register': 420, 'mapping': 'Phase 1 Real Power', 'units': 'watts'},
                 {'register': 421, 'mapping': 'Phase 2 Real Power', 'units': 'watts'},
                 {'register': 422, 'mapping': 'Phase 3 Real Power', 'units': 'watts'},
                 {'register': 423, 'mapping': 'Phase 4 Real Power', 'units': 'watts'},
                 {'register': 424, 'mapping': 'Phase 5 Real Power', 'units': 'watts'},
                 {'register': 425, 'mapping': 'Phase 6 Real Power', 'units': 'watts'},

                 {'register': 430, 'mapping': 'Phase 1 Apparent Power', 'units': 'volt-amps'},
                 {'register': 431, 'mapping': 'Phase 2 Apparent Power', 'units': 'volt-amps'},
                 {'register': 432, 'mapping': 'Phase 3 Apparent Power', 'units': 'volt-amps'},
                 {'register': 433, 'mapping': 'Phase 4 Apparent Power', 'units': 'volt-amps'},
                 {'register': 434, 'mapping': 'Phase 5 Apparent Power', 'units': 'volt-amps'},
                 {'register': 435, 'mapping': 'Phase 6 Apparent Power', 'units': 'volt-amps'},

                 {'register': 440, 'mapping': 'Phase 1 Power Factor', 'units': '%'},
                 {'register': 441, 'mapping': 'Phase 2 Power Factor', 'units': '%'},
                 {'register': 442, 'mapping': 'Phase 3 Power Factor', 'units': '%'},
                 {'register': 443, 'mapping': 'Phase 4 Power Factor', 'units': '%'},
                 {'register': 444, 'mapping': 'Phase 5 Power Factor', 'units': '%'},
                 {'register': 445, 'mapping': 'Phase 6 Power Factor', 'units': '%'},

                 {'register': 470, 'mapping': 'Phase 1 Balance', 'units': '%'},
                 {'register': 471, 'mapping': 'Phase 2 Balance', 'units': '%'},
                 {'register': 472, 'mapping': 'Phase 3 Balance', 'units': '%'},
                 {'register': 473, 'mapping': 'Phase 4 Balance', 'units': '%'},
                 {'register': 474, 'mapping': 'Phase 5 Balance', 'units': '%'},
                 {'register': 475, 'mapping': 'Phase 6 Balance', 'units': '%'},
                 ]
device_port = 502


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
