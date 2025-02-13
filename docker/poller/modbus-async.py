import pymodbus.client as ModbusClient
import asyncio
import datetime
from prometheus_client import start_http_server, disable_created_metrics, Gauge
import time
import requests
import logging
## prometheus setup



#logging
logging.basicConfig(filename="output.log",
                    format='%(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.INFO)


class Device():
    def __init__(self, name, ip, port, poll_type, power_limit, registers):
        self.name = name
        self.ip = ip
        self.port = int(port)
        self.poll_type = poll_type
        self.power_limit = int(power_limit)
        self.registers = registers

    async def pdu_read(self):
        try:
            client = ModbusClient.AsyncModbusTcpClient(self.ip, port=self.port,timeout=10)
            connection = await client.connect()
            if connection:
                for register in self.registers:
                    response = await client.read_holding_registers(int(register['register']), count=int(register["read_count"]), slave=int(register['slave']))
                    if response.isError():
                        logger.error(f'Modbus Error')
                    else:
                        logger.info(f'value: {response.registers[0]} metric: {register['metric_name']}')
                        gauge_key = f'{register['metric_name']}'
                        gauges[gauge_key].labels(device_name=self.name).set(response.registers[0])
            client.close()
        except Exception as e:
            print(f"Error:{e}")
            logger.error(f"Error:{e}")

    
    def create_read_task(self):
        task = asyncio.create_task(self.pdu_read())
        return task


async def poll_devices():
    asyncio_tasks = []
    for device in devices:
        asyncio_tasks.append(device.create_read_task())
    return await asyncio.wait(asyncio_tasks)


def get_devices():
    response = requests.get(f'http://flask:8000/devices/get_all_modbus')
    # logger.info(f'{response.json()}')
    device_list = []
    if response.status_code == 200:
        for device in response.json():
            device_list.append(Device(name=device['device_name'], ip=device['device_ip'], port=device['device_port'], poll_type=device['device_poll_type'],
                                  power_limit=device['device_power_limit'], registers=device['device_registers']))
            for register in device['device_registers']:
                try:
                    gauge_key = f'{register["metric_name"]}'
                    if gauge_key not in gauges:
                        gauges[gauge_key] = Gauge(register['metric_name'], "", labelnames=(['device_name']))
                except:
                    logger.error(f"error creating label {register['metric_name']}")
                
    return device_list

#prometheus setup
disable_created_metrics()
gauges = {}
start_http_server(8000)


# Output from get_devices()
# [{'_id': {'$oid': '67acf6f74cbee6b78db9e15a'}, 'device_name': '1400N 100E B', 'device_ip': '10.11.82.11', 'device_port': '502', 'device_poll_type': 'modbus', 
#  'device_power_limit': '6240', 'device_registers': [{'register': '299', 'read_count': '1', 'slave': '1', 'metric_name': 'Total Real Power', 'metric_unit': 'watts'},
#  {'register': '300', 'read_count': '1', 'slave': '1', 'metric_name': 'Total Apparent Power', 'metric_unit': 'volt-amps'}]}, {'_id': {'$oid': '67acf74b4cbee6b78db9e15b'},
#  'device_name': '1400N 100E C', 'device_ip': '10.11.82.12', 'device_port': '502', 'device_poll_type': 'modbus', 'device_power_limit': '6240', 'device_registers': 
# [{'register': '299', 'read_count': '1', 'slave': '1', 'metric_name': 'Total Real Power', 'metric_unit': 'watts'}, {'register': '300', 'read_count': '1', 'slave': '1', 
# 'metric_name': 'Total Apparent Power', 'metric_unit': 'volt-amps'}]}]

while True:
    devices = get_devices()
    logger.info(f'{devices}')
    asyncio.run(poll_devices())
    time.sleep(60)

