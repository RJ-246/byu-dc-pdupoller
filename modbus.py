import pymodbus.client as ModbusClient


pdu_ips = ['10.11.82.11', '10.11.82.12', '10.11.82.13', '10.11.82.14', '10.11.82.15','10.11.82.16','10.11.82.17', '10.11.82.18', '10.11.82.19', '10.11.82.20', '10.11.82.21',
           '10.11.82.22', '10.11.82.23', '10.11.82.24', '10.11.82.25', '10.11.82.26', '10.11.82.27', '10.11.82.28', '10.11.82.29', '10.11.82.30', '10.11.82.31', '10.11.82.32',
           '10.11.82.33', '10.11.82.34', '10.11.82.35', '10.11.82.36', '10.11.82.37', '10.11.82.38']
device_ip = '10.11.82.24'
device_port = 502

try:
    client = ModbusClient.ModbusTcpClient(device_ip, port=device_port, timeout = 10)
    connection = client.connect()

    if connection:
        print('connected')
        print(connection)
        response = client.read_holding_registers(409, 1, unit=1)
       
        if response.isError():
            print(f"Modbus error")
            print(response)
        else:
            print(response.registers[0]/100)

    client.close()
    print('client closed')
except Exception as e:
    print(f"Error: {e}")