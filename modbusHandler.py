from pymodbus.client.sync import ModbusSerialClient
import threading
import queue
import copy
import time

class ModbusResponseBuffer() :
    def __init__(self, identifier : str, slaveId : int, register : list) -> None:
        self.identifier : str = identifier
        self.slaveId : int = slaveId
        self.register : list = copy.deepcopy(register)
    
    def print(self):
        print("Received data")
        print("Identifier :", self.identifier)
        print("Slave Id :", self.slaveId)
        print("Register content :", self.register)

class Info() : 
    def __init__(self) -> None:
        self.slaveId : int = 0
        self.counter : int = 0
        self.batCapacity : int = 0
        self.batVoltage : int = 0
        self.chargeCurrent : int = 0
        self.controllerTemperature : int = 0
        self.batteryTemperature : int = 0
        self.loadVoltage : int = 0
        self.loadCurrent : int = 0
        self.loadPower : int = 0
        self.pvVoltage : int = 0
        self.pvCurrent : int = 0
        self.pvPower : int = 0
        self.loadStatus : int = 0

    def print(self):
        print("slave id :", self.slaveId)
        print("counter :", self.counter)
        print("battery capacity :", self.batCapacity)
        print("battery voltage :", self.batVoltage)
        print("charge current :", self.chargeCurrent)
        print("controller temperature :", self.controllerTemperature)
        print("battery temperature :", self.batteryTemperature)
        print("load voltage :", self.loadVoltage)
        print("load current :", self.loadCurrent)
        print("load power :", self.loadPower)
        print("pv voltage :", self.pvVoltage)
        print("pv current :", self.pvCurrent)
        print("pv power :", self.pvPower)
        print("pv load status :", self.loadStatus)

class Setting() : 
    def __init__(self) -> None:
        self.slaveId : int = 0
        self.counter : int = 0
        self.overVoltageThreshold = 0
        self.chargingLimitVoltage = 0
        self.equalizingChargingVoltage = 0
        self.boostChargingVoltage = 0
        self.floatingChargingVoltage = 0
        self.boostChargingRecoveryVoltage = 0
        self.overDischargeRecoveryVoltage = 0
        self.underVoltageThreshold = 0
        self.overDischargeVoltage = 0
        self.overDischargeLimitVoltage = 0
        self.endOfCharge = 0
        self.endOfDischarge = 0
        self.overDischargeTimeDelay = 0
        self.equalizingChargingTime = 0
        self.boostChargingTime = 0
        self.equalizingChargingInterval = 0
        self.temperatureCompensation = 0

    def print(self):
        print("slave id :", self.slaveId)
        print("counter :", self.counter)
        print("overvoltage threshold :", self.overVoltageThreshold)
        print("charging limit voltage :", self.chargingLimitVoltage)
        print("equalizing charging voltage :", self.equalizingChargingVoltage)
        print("boost charging voltage :", self.boostChargingVoltage)
        print("floating charging voltage :", self.floatingChargingVoltage)
        print("boost charging recovery voltage :", self.boostChargingRecoveryVoltage)
        print("over discharge recovery voltage :", self.overDischargeRecoveryVoltage)
        print("undervoltage threshold :", self.underVoltageThreshold)
        print("overdischarge voltage :", self.overDischargeVoltage)
        print("overdischarge limit voltage :", self.overDischargeLimitVoltage)
        print("end of charge :", self.endOfCharge)
        print("end of discharge :", self.endOfDischarge)
        print("overdischarge time delay:", self.overDischargeTimeDelay)
        print("equalizing charging time :", self.equalizingChargingTime)
        print("boost charging time :", self.boostChargingTime)
        print("equalizing charging interval :", self.equalizingChargingInterval)
        print("temperature compensation :", self.temperatureCompensation)

class MpptData() :
    def __init__(self, modbusResponseBuffer : ModbusResponseBuffer) -> None:
        self.slaveId : int = 0
        self.info : Info = None
        self.setting : Setting = None
        self.buildData(modbusResponseBuffer)

    def print(self):
        if (self.info is not None) :
            self.info.print()
        if (self.setting is not None) :
            self.setting.print()

    def buildData(self, modbusResponseBuffer : ModbusResponseBuffer) :
        if (modbusResponseBuffer.identifier == "batt_load_solar_info") :
            print("info")
            info = Info() 
            self.slaveId = modbusResponseBuffer.slaveId
            info.slaveId = modbusResponseBuffer.slaveId
            info.batCapacity = modbusResponseBuffer.register[0]
            info.batVoltage = modbusResponseBuffer.register[1]
            info.chargeCurrent = modbusResponseBuffer.register[2]
            info.controllerTemperature = modbusResponseBuffer.register[3] >> 8
            info.batteryTemperature = modbusResponseBuffer.register[3] & 0xFF
            info.loadVoltage = modbusResponseBuffer.register[4]
            info.loadCurrent = modbusResponseBuffer.register[5]
            info.loadPower = modbusResponseBuffer.register[6]
            info.pvVoltage = modbusResponseBuffer.register[7]
            info.pvCurrent = modbusResponseBuffer.register[8]
            info.pvPower = modbusResponseBuffer.register[9]
            info.loadStatus = modbusResponseBuffer.register[10]
            self.info = copy.deepcopy(info)
        elif (modbusResponseBuffer.identifier == "battery_setting") :
            print("setting")
            setting = Setting()
            self.slaveId = modbusResponseBuffer.slaveId
            setting.slaveId = modbusResponseBuffer.slaveId
            setting.overVoltageThreshold = modbusResponseBuffer.register[0]
            setting.chargingLimitVoltage = modbusResponseBuffer.register[1]
            setting.equalizingChargingVoltage = modbusResponseBuffer.register[2]
            setting.boostChargingVoltage = modbusResponseBuffer.register[3]
            setting.floatingChargingVoltage = modbusResponseBuffer.register[4]
            setting.boostChargingRecoveryVoltage = modbusResponseBuffer.register[5]
            setting.overDischargeRecoveryVoltage = modbusResponseBuffer.register[6]
            setting.underVoltageThreshold = modbusResponseBuffer.register[7]
            setting.overDischargeVoltage = modbusResponseBuffer.register[8]
            setting.overDischargeLimitVoltage = modbusResponseBuffer.register[9]
            setting.endOfCharge = modbusResponseBuffer.register[10] >> 8
            setting.endOfDischarge = modbusResponseBuffer.register[10] & 0xFF
            setting.overDischargeTimeDelay = modbusResponseBuffer.register[11]
            setting.equalizingChargingTime = modbusResponseBuffer.register[12]
            setting.boostChargingTime = modbusResponseBuffer.register[13]
            setting.equalizingChargingInterval = modbusResponseBuffer.register[14]
            setting.temperatureCompensation = modbusResponseBuffer.register[15]
            self.setting = copy.deepcopy(setting)
        else :
            print("Unidentified identifier")

class MpptDataCollection() :
    def __init__(self) -> None:
        self.infoList : list[Info] = []
        self.settingList : list[Setting] = []

    def print(self) :
        for element in self.infoList :
            element.print()
        for element in self.settingList :
            element.print()

    def insertData(self, mpptData : MpptData) -> None:

        print("info length :", len(self.infoList))
        print("setting length :", len(self.settingList))

        if (mpptData.info is not None) :
            for index, element in enumerate(self.infoList) :
                if element.slaveId == mpptData.slaveId :
                    self.infoList[index].slaveId = element.slaveId
                    self.infoList[index].counter += 1
                    self.infoList[index].batCapacity = element.batCapacity
                    self.infoList[index].batVoltage = element.batVoltage
                    self.infoList[index].chargeCurrent = element.chargeCurrent
                    self.infoList[index].controllerTemperature = element.controllerTemperature
                    self.infoList[index].batteryTemperature = element.batteryTemperature
                    self.infoList[index].loadVoltage = element.loadVoltage
                    self.infoList[index].loadCurrent = element.loadCurrent
                    self.infoList[index].loadPower = element.loadPower
                    self.infoList[index].pvVoltage = element.pvVoltage
                    self.infoList[index].pvCurrent = element.pvCurrent
                    self.infoList[index].pvPower = element.pvPower
                    self.infoList[index].loadStatus = element.loadStatus
                    return
            self.infoList.append(mpptData.info)
        
        if (mpptData.setting is not None) :
            for index, element in enumerate(self.settingList) :
                if element.slaveId == mpptData.slaveId :
                    self.settingList[index].slaveId = element.slaveId
                    self.settingList[index].counter += 1
                    self.settingList[index].overVoltageThreshold = element.overVoltageThreshold
                    self.settingList[index].chargingLimitVoltage = element.chargingLimitVoltage
                    self.settingList[index].equalizingChargingVoltage = element.equalizingChargingVoltage
                    self.settingList[index].boostChargingVoltage = element.boostChargingVoltage
                    self.settingList[index].floatingChargingVoltage = element.floatingChargingVoltage
                    self.settingList[index].boostChargingRecoveryVoltage = element.boostChargingRecoveryVoltage
                    self.settingList[index].overDischargeRecoveryVoltage = element.overDischargeRecoveryVoltage
                    self.settingList[index].underVoltageThreshold = element.underVoltageThreshold
                    self.settingList[index].overDischargeVoltage = element.overDischargeVoltage
                    self.settingList[index].overDischargeLimitVoltage = element.overDischargeLimitVoltage
                    self.settingList[index].endOfCharge = element.endOfCharge
                    self.settingList[index].endOfDischarge = element.endOfDischarge
                    self.settingList[index].overDischargeTimeDelay = element.overDischargeTimeDelay
                    self.settingList[index].equalizingChargingTime = element.equalizingChargingTime
                    self.settingList[index].boostChargingTime = element.boostChargingTime
                    self.settingList[index].equalizingChargingInterval = element.equalizingChargingInterval
                    self.settingList[index].temperatureCompensation = element.temperatureCompensation
                    return
            self.settingList.append(mpptData.setting)

    def getInfo(self) -> list[dict] :
        result : list[dict] = []
        for element in self.infoList :
            dataDict :dict = {
                "slave_id" : element.slaveId,
                "counter" : element.counter,
                "battery_capacity" : element.batCapacity,
                "battery_voltage" : element.batVoltage,
                "charge_current" : element.chargeCurrent,
                "controller_temperature" : element.controllerTemperature,
                "battery_temperature" : element.batteryTemperature,
                "load_voltage" : element.loadVoltage,
                "load_current" : element.loadCurrent,
                "load_power" : element.loadPower,
                "pv_voltage" : element.pvVoltage,
                "pv_current" : element.pvCurrent,
                "pv_power" : element.pvPower,
                "load_status" : element.loadStatus
            }
            result.append(dataDict)
        return result
    
    def getSetting(self) -> list[dict] :
        result : list[dict] = []
        for element in self.settingList :
            dataDict :dict = {
                "slave_id" : element.slaveId,
                "counter" : element.counter,
                "over_voltage_threshold" : element.overVoltageThreshold,
                "charging_limit_voltage" : element.chargingLimitVoltage,
                "equalizing_charging_voltage" : element.equalizingChargingVoltage,
                "boost_charging_voltage" : element.boostChargingVoltage,
                "floating_charging_voltage" : element.floatingChargingVoltage,
                "boost_charging_recovery_voltage" : element.boostChargingRecoveryVoltage,
                "overdischarge_recovery_voltage" : element.overDischargeRecoveryVoltage,
                "undervoltage_threshold" : element.underVoltageThreshold,
                "overdischarge_voltage" : element.overDischargeVoltage,
                "overdischarge_limit_voltage" : element.overDischargeLimitVoltage,
                "end_of_charge" : element.endOfCharge,
                "end_of_discharge" : element.endOfDischarge,
                "overdischarge_time_delay" : element.overDischargeTimeDelay,
                "equalizing_charging_time" : element.equalizingChargingTime,
                "boost_charging_time" : element.boostChargingTime,
                "equalizing_charging_interval" : element.equalizingChargingInterval,
                "temperature_compensation" : element.temperatureCompensation
            }
            result.append(dataDict)
        return result
    
    
        

class ModbusRegisterList() :
    """
    Class to convert the dict config file into slaveId, list of read register and list of write register
    """
    def __init__(self, configFile : dict) -> None:
        """Class initialization

        Args :
        configFile (dict) : config file as dict type file, refer to modbus_register_list.json
        """
        self.slaveid = configFile['slave_id']
        self.writeSection : list[dict] = []
        for element in configFile['write_section'] :
            self.writeSection.append(element)
        self.readSection : list[dict] = []
        for element in configFile['read_section'] :
            self.readSection.append(element)

    def printAll(self) :
        """
        Print the parsed config file
        """
        print(self.slaveid)
        for element in self.readSection :
            print(element)
        for element in self.writeSection :
            print(element)

class ModbusMessage() :
    """ ModbusMessage class that contain the slaveid, register name, and value. 
    This message will pass into ModbusHandler to be processed
    """
    def __init__(self, slaveId : int, name : str, value : int) -> None:
        """Class initialization

        Args :
        slaveId (int) : slave address destination
        name (str) : register name, refer to modbus_register_list on write_section key
        value (int) : value to be written into register
        """
        self.slaveId = slaveId
        self.name = name
        self.value = value

class ModbusHandler(threading.Thread) :
    """ ModbusHandler is a thread class that handle the reading and writing of modbus data. Treat this class as a threading.Thread
    """
    def __init__(self, modbusRegisterList : list[ModbusRegisterList]):
        """ Class initialization
        
        Args:
        modbusRegisterList (list[ModbusRegisterList]) : list of ModbusRegisterList, this argument is a guide book to which register to read and write
        """
        threading.Thread.__init__(self)
        self.mpptDataCollection : MpptDataCollection = MpptDataCollection()
        self.modbusSerialClient : ModbusSerialClient = None
        self.daemon = True
        self.isRun = False
        self.writeQueue = queue.Queue()
        self.modbusRegisterList : list[ModbusRegisterList] = copy.deepcopy(modbusRegisterList)
        self.inc = 0

    def putToQueue(self, modbusMessage : ModbusMessage) :
        """ Put the modbus message into class queue to be further processed
        
        Args :
        modbusMessage(ModbusMessage) : modbusMessage, refer into ModbusMessage class
        """
        self.writeQueue.put(modbusMessage)

    def setModbus(self, modbusSerialClient : ModbusSerialClient) :
        """ Register the modbus serial object, before run this class thread, 
        set the modbus serial object first or else the data won't send into serial port line
        
        Args :
        modbusSerialClient (ModbusSerialClient) : modbus serial object, refer to ModbusSerialClient
        """
        self.modbusSerialClient = modbusSerialClient

    def run(self) :
        self.isRun = True
        while self.isRun :
            if self.inc >= len(self.modbusRegisterList) :
                self.inc = 0
            
            while not self.writeQueue.empty() : #check if the writequeue not empty
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
                # print("Slave id :", element.slaveid)
                # print("Name :", read['name'])
                # print("register :", read['start_register'])
                # print("quantity :", read['quantity'])
                # self.modbusSerialClient.connect()
                try :
                    self.modbusSerialClient.connect()
                    rr = self.modbusSerialClient.read_holding_registers(read['start_register'], read['quantity'], unit = element.slaveid)
                    self.modbusSerialClient.close()
                    mb = ModbusResponseBuffer(read['name'], element.slaveid, rr.registers)
                    md = MpptData(mb)
                    self.mpptDataCollection.insertData(md)
                    print()
                except :
                    print("failed to request modbus")
                time.sleep(0.2)
            self.inc += 1
    
    def getWriteRegisterAddress(self, modbusMessage : ModbusMessage) -> int :
        """ Get the address of register. Since the ModbusMessage contain only register name not the address, it need to search the suitable address
        
        Args :
        modbusMessage (ModbusMessage) : refer to ModbusMessage class. contain the register name, slaveid and value
        
        Returns :
        int : register address
        """
        for element in self.modbusRegisterList :
            if element.slaveid == modbusMessage.slaveId :
                for write in element.writeSection :
                    if modbusMessage.name == write['name'] :
                        return write['start_register']
        return -1

    def stop(self) :
        self.isRun = False

