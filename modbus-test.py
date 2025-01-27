import pymodbus.client as ModbusClient
import time

device_ip = "10.26.58.31"
device_register = 13
register_count = 4
device_port = 502

try:
    client = ModbusClient.ModbusTcpClient(device_ip, port=device_port,timeout=10)
    startTime = time.time()
    connection = client.connect()
    if connection:
        response =  client.read_holding_registers(device_register, slave=31, count=register_count)
        endTime = time.time()
        if response.isError():
            print(f"Modbus Error")
        else:
            print(f'value: {response}')
            print(f'Response Time: {endTime - startTime}')
    client.close()
except Exception as e:
    print(f"Error:{e}")