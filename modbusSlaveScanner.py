from pymodbus.client.sync import ModbusSerialClient

class ModbusSlaveScanner() :
    def __init__(self, method : str = 'rtu', port : str = 'COM1', timeout : float = 0.1, baudrate : int = 9600) -> None:
        self.startId = 1
        self.endId = 247
        self.registerAddress = 1
        self.method = method
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def startScan(self) -> list :
        client = ModbusSerialClient(method=self.method, port=self.port, timeout=self.timeout, baudrate=self.baudrate)
        slaveList : list = []
        print("Start slave scan")
        for i in range(self.startId,self.endId,1) :
            client.connect()
            rr = client.read_holding_registers(address=self.registerAddress, count=1, unit=i)
            if (rr.isError()) :
                print(f"Slave id {i} not found")
                client.close()    
                continue
            print(f"Slave id {i} found")
            slaveList.append(i)
            client.close()
        print("Slave scan finished")
        return slaveList
