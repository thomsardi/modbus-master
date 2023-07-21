from modbusSlaveScanner import ModbusSlaveScanner

class MpptSrne(ModbusSlaveScanner) :
    def __init__(self, method: str = 'rtu', port: str = 'COM1', timeout: float = 0.1, baudrate: int = 9600) -> None:
        super().__init__(method, port, timeout, baudrate)
        self.registerAddress = 257

class MpptEpever(ModbusSlaveScanner) :
    def __init__(self, method: str = 'rtu', port: str = 'COM1', timeout: float = 0.1, baudrate: int = 9600) -> None:
        super().__init__(method, port, timeout, baudrate)
        self.registerAddress = 257