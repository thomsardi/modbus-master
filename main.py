from pymodbus.client.sync import ModbusSerialClient
from modbusHandler import ModbusHandler, ModbusRegisterList, ModbusMessage
from mppt import MpptSrne
import json
import time
from httpserver import Server
from typing import List

print("Modbus Handler for Python3.7.3")

def main() :
    registerListFile = json.load(open('modbus_register_list.json')) #convert the json file into dict
    registerList = registerListFile['device'] #get the content of 'device' key
    # configFile = json.load(open('modbus_config.json'))
    configFile = json.load(open('modbus_config_test.json')) #convert the json file into dict
    config = configFile['config'] #get the content of 'config' key
    portName = configFile['port_name'] #get the content of 'port_name' key
    isUpdate = configFile['update'] #get the content of 'update' key
    modbusRegisterList : List[ModbusRegisterList] = [] #create list
    # client = ModbusSerialClient(method='rtu', port='COM7', timeout=1, baudrate=9600)
    client = ModbusSerialClient(method='rtu', port=portName, timeout=1, baudrate=9600) #create ModbusSerialClient object with rtu method, 8,N,1,9600
    for element in registerList :
        mc = ModbusRegisterList(element) #convert the formatted dict into ModbusRegisterList
        modbusRegisterList.append(mc) #append the ModbusRegisterList

    modbusHandler = ModbusHandler(modbusRegisterList) #create ModbusHandler object
    modbusHandler.setModbus(client) #register the ModbusSerialClient into ModbusHandler
    
    """
    to update parameter, isUpdate flag, register name and value is taken from modbus_config.json
    register name must be within modbus_register_list.json or else it fails to update
    """
    if(isUpdate > 0) :
        print("Updating parameter...")
        for element in config :
            id = element['slave_id']
            param = element['param']
            for p in param :
                modbusHandler.putToQueue(ModbusMessage(id, p['name'], p['value'])) #put the ModbusMessage into ModbusHandler queue

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

def scanSlave(method : str, portName : str, timeout : float, baudrate : int) -> list :
    client = ModbusSerialClient(method=method, port=portName, timeout=timeout, baudrate=baudrate)
    slaveList : list = []
    print("Start slave scan")
    for i in range(1,247,1) :
        client.connect()
        rr = client.read_holding_registers(address=257, count=1, unit=i)
        if (rr.isError()) :
            print(f"Slave id {i} not found")
            client.close()    
            continue
        print(f"Slave id {i} found")
        slaveList.append(i)
        client.close()
    print("Slave scan finished")
    return slaveList

if __name__ == "__main__" :
    
    registerListFile = json.load(open('modbus_register_list.json')) #convert the json file into dict
    registerList = registerListFile['device'] #get the content of 'device' key
    # configFile = json.load(open('modbus_config.json'))
    configFile = json.load(open('modbus_config_test.json')) #convert the json file into dict
    config = configFile['config'] #get the content of 'config' key
    portName = configFile['port_name'] #get the content of 'port_name' key
    isUpdate = configFile['update'] #get the content of 'update' key
    modbusRegisterList : List[ModbusRegisterList] = [] #create list
    # client = ModbusSerialClient(method='rtu', port='COM7', timeout=1, baudrate=9600)
    # print(scanSlave('rtu', portName=portName, timeout=0.05, baudrate=9600))
    # scanner = MpptSrne(method='rtu', port=portName, timeout=0.05, baudrate=9600)
    # print(scanner.startScan())
    client = ModbusSerialClient(method='rtu', port=portName, timeout=1, baudrate=9600) #create ModbusSerialClient object with rtu method, 8,N,1,9600
    for element in registerList :
        mc = ModbusRegisterList(element) #convert the formatted dict into ModbusRegisterList
        modbusRegisterList.append(mc) #append the ModbusRegisterList
    
    modbusHandler = ModbusHandler(modbusRegisterList) #create ModbusHandler object
    modbusHandler.setModbus(client) #register the ModbusSerialClient into ModbusHandler

    server = Server("httpThread", modbusHandler.mpptDataCollection, modbusHandler)

    """
    to update parameter, isUpdate flag, register name and value is taken from modbus_config.json
    register name must be within modbus_register_list.json or else it fails to update
    """
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
    server.start()
    count = 0
    while(1) :
        time.sleep(0.1)
        # print("length :", len(modbusHandler.mpptDataCollection.infoList))
        count += 1
        if count >= 50 :
            modbusHandler.mpptDataCollection.cleanUp()
            count = 0
            pass
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
    