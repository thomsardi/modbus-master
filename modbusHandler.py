from pymodbus.client.sync import ModbusSerialClient
import threading
import queue
import json
import copy
import time

class ModbusRegisterList() :
    def __init__(self, configFile : dict) -> None:
        self.slaveid = configFile['slave_id']
        self.writeSection : list[dict] = []
        for element in configFile['write_section'] :
            self.writeSection.append(element)
        self.readSection : list[dict] = []
        for element in configFile['read_section'] :
            self.readSection.append(element)

    def printAll(self) :
        print(self.slaveid)
        for element in self.readSection :
            print(element)
        for element in self.writeSection :
            print(element)

class ModbusMessage() :
    def __init__(self, slaveId : int, name : str, value : int) -> None:
        self.slaveId = slaveId
        self.name = name
        self.value = value

class ModbusHandler(threading.Thread) :
    def __init__(self, modbusRegisterList : list[ModbusRegisterList]):
        threading.Thread.__init__(self)
        self.modbusSerialClient : ModbusSerialClient = None
        self.daemon = True
        self.isRun = False
        self.writeQueue = queue.Queue()
        self.modbusRegisterList : list[ModbusRegisterList] = copy.deepcopy(modbusRegisterList)
        self.inc = 0

    def putToQueue(self, modbusMessage : ModbusMessage) :
        self.writeQueue.put(modbusMessage)

    def setModbus(self, modbusSerialClient : ModbusSerialClient) :
        self.modbusSerialClient = modbusSerialClient

    def run(self) :
        self.isRun = True
        while self.isRun :
            if self.inc >= len(self.modbusRegisterList) :
                self.inc = 0
            
            while not self.writeQueue.empty() :
                message : ModbusMessage = self.writeQueue.get()
                startRegister = self.getWriteRegisterAddress(message)
                print("Slave Id : ", message.slaveId)
                print("Name :", message.name)
                print("Register Addr :", startRegister)
                print("Value :", message.value)
                if (self.modbusSerialClient) is not None :
                    if (startRegister > 0) :
                        self.modbusSerialClient.connect()
                        rq = self.modbusSerialClient.write_register(startRegister, message.value, unit=message.slaveId)
                        print(rq)
                        self.modbusSerialClient.close()
                    # self.modbusSerialClient.connect()
                    # rr = self.modbusSerialClient.write_register(message.slaveId,)
                time.sleep(0.2)
            
            element = self.modbusRegisterList[self.inc]
            
            for read in element.readSection :
                print("Slave id :", element.slaveid)
                print("Name :", read['name'])
                print("register :", read['start_register'])
                print("quantity :", read['quantity'])
                # self.modbusSerialClient.connect()
                try :
                    self.modbusSerialClient.connect()
                    rr = self.modbusSerialClient.read_holding_registers(read['start_register'], read['quantity'], unit = element.slaveid)
                    self.modbusSerialClient.close()
                    print(rr.registers)
                except :
                    print("failed to request modbus")
                time.sleep(0.2)
            self.inc += 1
    
    def getWriteRegisterAddress(self, modbusMessage : ModbusMessage) -> int :
        for element in self.modbusRegisterList :
            if element.slaveid == modbusMessage.slaveId :
                for write in element.writeSection :
                    if modbusMessage.name == write['name'] :
                        return write['start_register']
        return -1

    def stop(self) :
        self.isRun = False

class ModbusBuffer() :
    def __init__(self) -> None:
        pass