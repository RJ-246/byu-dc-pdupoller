import pymodbus.client as ModbusClient
import asyncio
import datetime
from prometheus_client import start_http_server, disable_created_metrics, Gauge
import time
import requests
import logging
## prometheus setup
disable_created_metrics()

gauges = {}


#logging
logging.basicConfig(filename="output.log",
                    format='%(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.INFO)


class Device():
    def __init__(self, name, ip,values_to_poll, port, poll_type, power_limit):
        self.name = name
        self.ip = ip
        self.port = port
        self.values_to_poll = values_to_poll
        self.poll_type = poll_type
        self.port = 502
        self.power_limit = power_limit
        self.registers = self.registers

    async def pdu_read(self):
        try:
            client = ModbusClient.AsyncModbusTcpClient(self.ip, port=self.port,timeout=10)
            connection = await client.connect()
            if connection:
                for register in self.registers:
                    response = await client.read_holding_registers(register['register'], count=register["read_count"])
                    if response.isError():
                        print(f"Modbus Error")
                    else:
                        print(f'value: {response.registers[0]}')
                        gauge_key = f'{register['metric_name']}'
                        gauges[gauge_key].labels(device_name=self.name).set(response.registers[0])
            client.close()
        except Exception as e:
            print(f"Error:{e}")

    
    def create_read_task(self):
        task = asyncio.create_task(self.pdu_read())
        return task



#All IPs for PDUs
pdu_ips = [{'ip': '10.11.82.11', 'name': '1400N_100E_B'}, {'ip': '10.11.82.12', 'name': '1400N_100E_C'}, {'ip': '10.11.82.13', 'name': '1400N_200E_B'},
           {'ip': '10.11.82.14', 'name': '1400N_200E_C'}, {'ip': '10.11.82.15', 'name': '1400N_300E_B'}, {'ip': '10.11.82.16', 'name': '1400N_300E_C'},
           {'ip': '10.11.82.17', 'name': '1400N_400E_B'}, {'ip': '10.11.82.18', 'name': '1400N_400E_C'}, {'ip': '10.11.82.19', 'name': '1400N_500E_B'},
           {'ip': '10.11.82.20', 'name': '1400N_500E_C'}, {'ip': '10.11.82.21', 'name': '1400N_600E_B'}, {'ip': '10.11.82.22', 'name': '1400N_600E_C'},
           {'ip': '10.11.82.23', 'name': '1400N_700E_A'},{'ip': '10.11.82.24', 'name': '1400N_700E_B'},

           {'ip': '10.11.82.47', 'name': '1300N_500E_B'}, {'ip': '10.11.82.48', 'name': '1300N_500E_C'}, {'ip': '10.11.82.49', 'name': '1300N_600E_A'},
           {'ip': '10.11.82.50', 'name': '1300N_600E_C'}, {'ip': '10.11.82.51', 'name': '1300N_700E_A'}, {'ip': '10.11.82.52', 'name': '1300N_700E_C'},
           
           {'ip': '10.11.82.25', 'name': '900N_100E_A'}, {'ip': '10.11.82.26', 'name': '900N_100E_B'}, {'ip':'10.11.82.27', 'name': '900N_200E_A'},
           {'ip': '10.11.82.28' ,'name': '900N_200E_B'}, {'ip': '10.11.82.29','name': '900N_300E_A'}, {'ip': '10.11.82.30','name': '900N_300E_B'},
           {'ip': '10.11.82.31','name': '900N_400E_A'}, {'ip': '10.11.82.32','name':'900N_400E_B'}, {'ip': '10.11.82.33','name':'900N_500E_A'},
           {'ip': '10.11.82.34','name':'900N_500E_B'}, {'ip': '10.11.82.35','name':'900N_600E_B'}, {'ip': '10.11.82.36','name':'900N_600E_C'},
           {'ip': '10.11.82.37','name':'900N_700E_A'}, {'ip': '10.11.82.38','name':'900N_700E_B'},
           
           ]

#The registers to read data from (each pdu has a CSV you can download with the register metric_names)
pdu_registers = [{'register': 299, 'metric_name': 'pdu_real_power_watts_total', 'units': 'watts', 'count': 1},
                 {'register': 300, 'metric_name': 'pdu_apparent_power_voltamps_total', 'units': 'volt-amps', 'count': 1},
                 {'register': 301, 'metric_name': 'pdu_power_factor_total', 'units': '%', 'count': 1},
                 {'register': 302, 'metric_name': 'pdu_energy_kilowatthours_total', 'units': 'kilowatt-hours', 'count': 1},

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


async def poll_devices():
    asyncio_tasks = []
    for device in devices:
        asyncio_tasks.append(device.create_read_task())
    return await asyncio.wait(asyncio_tasks)


def get_devices():
    mongo_address = 'pdu_poll-mongodb-1:27017'
    response = requests.get(f'http://{mongo_address}/devices/get_modbus_devices')
    logger.info(f'{response}')
    print(response)



start_http_server(8000)


devices = []
asyncio_tasks = []

#Get device list from mongoDB


for pdu in pdu_ips:
    devices.append(Device(ip=pdu['ip'], name=pdu['name'], values_to_poll=pdu_registers, poll_type="modbus"))
for reading in pdu_registers:
    gauge_key = f'{reading['metric_name']}'
    if gauge_key not in gauges:
        gauges[gauge_key] = Gauge(reading['metric_name'], "", ["device_name"])

while True:
    asyncio.run(poll_devices())
    get_devices()
    time.sleep(60)

