from pymodbus.client.sync import ModbusSerialClient
from modbusHandler import ModbusHandler, ModbusRegisterList, ModbusMessage
import json
import time

if __name__ == "__main__" :
    registerListFile = json.load(open('modbus_register_list.json'))
    registerList = registerListFile['device']
    # configFile = json.load(open('modbus_config.json'))
    configFile = json.load(open('modbus_config_test.json'))
    config = configFile['config']
    portName = configFile['port_name']
    isUpdate = configFile['update']
    modbusRegisterList : list[ModbusRegisterList] = []
    # client = ModbusSerialClient(method='rtu', port='COM7', timeout=1, baudrate=9600)
    client = ModbusSerialClient(method='rtu', port=portName, timeout=1, baudrate=9600)
    for element in registerList :
        mc = ModbusRegisterList(element)
        modbusRegisterList.append(mc)

    modbusHandler = ModbusHandler(modbusRegisterList)
    modbusHandler.setModbus(client)
    
    """to update parameter, isUpdate flag, register name and value is taken from modbus_config.json"""
    """register name must be within modbus_register_list.json or else it fails to update"""
    if(isUpdate > 0) :
        print("Updating parameter...")
        for element in config :
            id = element['slave_id']
            param = element['param']
            for p in param :
                modbusHandler.putToQueue(ModbusMessage(id, p['name'], p['value']))

    # modbusHandler.putToQueue(ModbusMessage(172, "system_voltage", 1500))
    # modbusHandler.putToQueue(ModbusMessage(172, "overvoltage_threshold", 2000))
    # modbusHandler.putToQueue(ModbusMessage(172, "floating_charging_voltage", 3000))
    
    modbusHandler.start()
    while(1) :
        time.sleep(0.1)
    # modbusHandler.stop()

    
    
    # client.connect()
    # rr = client.read_holding_registers(256,10, unit=172)
    # print(rr.registers)
    # client.close()

    # print("asdaw")
    # run_sync_client("127.0.0.1", "COM7")
    # run_sync_client("127.0.0.1", "/dev/ttyS0")
    # c = ModbusSerialClient("COM7", framer=ModbusRtuFramer, baudrate=9600)
    # c.connect()
    # print(c.read_holding_registers(256,11,1).registers)
    # c.close()
    