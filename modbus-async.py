import pymodbus.client as ModbusClient
import influxdb_client, os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import asyncio
import datetime
from prometheus_client import start_http_server, disable_created_metrics

## prometheus setup
disable_created_metrics()


#Sets up influxDB info
# token = os.environ['INFLUX_TOKEN']
token = "abc"
influxdb_address = 'pdu_poll-influxdb-1:8086'
org='byu'
bucket = 'pdu-data'
url = f"http://{influxdb_address}"

influx_client = influxdb_client.InfluxDBClient(url=url,token=token,org=org)



class Device():
    def __init__(self, name, ip, values_to_poll, poll_type):
        self.name = name
        self.ip = ip
        self.values_to_poll = values_to_poll
        self.poll_type = poll_type

    async def create_read_task(self):
        task = asyncio.create_task(pdu_read(self))

#All IPs for PDUs
pdu_ips = [{'ip': '10.11.82.11', 'name': '1400N_100E_B'}, {'ip': '10.11.82.12', 'name': '1400N_100E_C'}, {'ip': '10.11.82.13', 'name': '1400N_200E_B'},
           {'ip': '10.11.82.14', 'name': '1400N_200E_C'}, {'ip': '10.11.82.15', 'name': '1400N_300E_B'}, {'ip': '10.11.82.16', 'name': '1400N_300E_C'},
           {'ip': '10.11.82.17', 'name': '1400N_400E_B'}, {'ip': '10.11.82.18', 'name': '1400N_400E_C'}, {'ip': '10.11.82.19', 'name': '1400N_500E_B'},
           {'ip': '10.11.82.20', 'name': '1400N_500E_C'}, {'ip': '10.11.82.21', 'name': '1400N_600E_B'}, {'ip': '10.11.82.22', 'name': '1400N_600E_C'},
           {'ip': '10.11.82.23', 'name': '1400N_700E_B'},{'ip': '10.11.82.24', 'name': '1400N_700E_C'},
           
           {'ip': '10.11.82.25', 'name': '900N_100E_A'}, {'ip': '10.11.82.26', 'name': '900N_100E_B'}, {'ip':'10.11.82.27', 'name': '900N_200E_A'},
           {'ip': '10.11.82.28' ,'name': '900N_200E_B'}, {'ip': '10.11.82.29','name': '900N_300E_A'}, {'ip': '10.11.82.30','name': '900N_300E_B'},
           {'ip': '10.11.82.31','name': '900N_400E_A'}, {'ip': '10.11.82.32','name':'900N_400E_B'}, {'ip': '10.11.82.33','name':'900N_500E_A'},
           {'ip': '10.11.82.34','name':'900N_500E_B'}, {'ip': '10.11.82.35','name':'900N_600E_B'}, {'ip': '10.11.82.36','name':'900N_600E_C'},
           {'ip': '10.11.82.37','name':'900N_700E_A'}, {'ip': '10.11.82.38','name':'900N_700E_B'}]

#The registers to read data from (each pdu has a CSV you can download with the register metric_names)
pdu_registers = [{'register': 299, 'metric_name': 'pdu_real_power_watts_total', 'units': 'watts'},
                 {'register': 300, 'metric_name': 'pdu_apparent_power_volt-amps_total', 'units': 'volt-amps'},
                 {'register': 301, 'metric_name': 'pdu_power_factor_total', 'units': '%'},
                 {'register': 302, 'metric_name': 'pdu_energy_kilowatt-hours_total', 'units': 'kilowatt-hours'},

                #  {'register': 400, 'metric_name': 'Phase 1 Voltage', 'units': 'volts'},
                #  {'register': 401, 'metric_name': 'Phase 2 Voltage', 'units': 'volts'},
                #  {'register': 402, 'metric_name': 'Phase 3 Voltage', 'units': 'volts'},
                #  {'register': 403, 'metric_name': 'Phase 4 Voltage', 'units': 'volts'},
                #  {'register': 404, 'metric_name': 'Phase 5 Voltage', 'units': 'volts'},
                #  {'register': 405, 'metric_name': 'Phase 6 Voltage', 'units': 'volts'},

                #  {'register': 410, 'metric_name': 'Phase 1 Current', 'units': 'amps'},
                #  {'register': 411, 'metric_name': 'Phase 2 Current', 'units': 'amps'},
                #  {'register': 412, 'metric_name': 'Phase 3 Current', 'units': 'amps'},
                #  {'register': 413, 'metric_name': 'Phase 4 Current', 'units': 'amps'},
                #  {'register': 414, 'metric_name': 'Phase 5 Current', 'units': 'amps'},
                #  {'register': 415, 'metric_name': 'Phase 6 Current', 'units': 'amps'},

                #  {'register': 420, 'metric_name': 'Phase 1 Real Power', 'units': 'watts'},
                #  {'register': 421, 'metric_name': 'Phase 2 Real Power', 'units': 'watts'},
                #  {'register': 422, 'metric_name': 'Phase 3 Real Power', 'units': 'watts'},
                #  {'register': 423, 'metric_name': 'Phase 4 Real Power', 'units': 'watts'},
                #  {'register': 424, 'metric_name': 'Phase 5 Real Power', 'units': 'watts'},
                #  {'register': 425, 'metric_name': 'Phase 6 Real Power', 'units': 'watts'},

                #  {'register': 430, 'metric_name': 'Phase 1 Apparent Power', 'units': 'volt-amps'},
                #  {'register': 431, 'metric_name': 'Phase 2 Apparent Power', 'units': 'volt-amps'},
                #  {'register': 432, 'metric_name': 'Phase 3 Apparent Power', 'units': 'volt-amps'},
                #  {'register': 433, 'metric_name': 'Phase 4 Apparent Power', 'units': 'volt-amps'},
                #  {'register': 434, 'metric_name': 'Phase 5 Apparent Power', 'units': 'volt-amps'},
                #  {'register': 435, 'metric_name': 'Phase 6 Apparent Power', 'units': 'volt-amps'},

                #  {'register': 440, 'metric_name': 'Phase 1 Power Factor', 'units': '%'},
                #  {'register': 441, 'metric_name': 'Phase 2 Power Factor', 'units': '%'},
                #  {'register': 442, 'metric_name': 'Phase 3 Power Factor', 'units': '%'},
                #  {'register': 443, 'metric_name': 'Phase 4 Power Factor', 'units': '%'},
                #  {'register': 444, 'metric_name': 'Phase 5 Power Factor', 'units': '%'},
                #  {'register': 445, 'metric_name': 'Phase 6 Power Factor', 'units': '%'},

                #  {'register': 470, 'metric_name': 'Phase 1 Balance', 'units': '%'},
                #  {'register': 471, 'metric_name': 'Phase 2 Balance', 'units': '%'},
                #  {'register': 472, 'metric_name': 'Phase 3 Balance', 'units': '%'},
                #  {'register': 473, 'metric_name': 'Phase 4 Balance', 'units': '%'},
                #  {'register': 474, 'metric_name': 'Phase 5 Balance', 'units': '%'},
                #  {'register': 475, 'metric_name': 'Phase 6 Balance', 'units': '%'},
                 ]
device_port = 502




async def pdu_read(pdu):
    try:
        data = []
        client = ModbusClient.AsyncModbusTcpClient(pdu['ip'], port=device_port,timeout=10)
        connection = await client.connect()

        if connection:
            for reading in pdu_registers:
                response = await client.read_holding_registers(reading['register'])
                if response.isError():
                    print(f"Modbus Error")
                else:
                    data.append({'value': response.registers[0], 'metric_name': reading['metric_name'], 'units': reading['units']})
        client.close()
        print(data)
        write_api = influx_client.write_api(write_options=SYNCHRONOUS)
        for point_value in data:
            point = (
                Point(point_value['metric_name'])
                .tag('pdu_name', pdu['name'])
                .field(point_value['units'], point_value['value'])
            )
            # write_api.write(bucket=bucket,org='byu',record=point)

    except Exception as e:
        print(f"Error:{e}")

async def read_pdu_data():
    tasks = [asyncio.create_task(pdu_read(pdu)) for pdu in pdu_ips]
    # for pdu in pdu_ips:
        # tasks = tasks.append(asyncio.create_task(pdu_read(pdu)))
    _ = await asyncio.wait(tasks)



curTime = datetime.datetime.now()
asyncio.run(read_pdu_data())
endTime = datetime.datetime.now()

devices = []
asyncio_tasks = []
for pdu in pdu_ips:
    devices.append(Device(ip=pdu.ip, name=pdu.name, values_to_poll=pdu_registers, poll_type="modbus"))
for device in devices:
    asyncio_tasks.append(device.create_read_task())


print(f'{endTime-curTime} Seconds')

