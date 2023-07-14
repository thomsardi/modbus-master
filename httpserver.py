import threading
from flask import Flask, request, make_response
import queue
from modbusHandler import MpptDataCollection, ModbusHandler, ModbusMessage

class Server(threading.Thread) :
    def __init__(self, name : str, data : MpptDataCollection, modbusHandler : ModbusHandler) :
        threading.Thread.__init__(self, name=name)
        self.daemon = True
        self.app = Flask(__name__)
        self.data : MpptDataCollection = data
        self.modbusHandler : ModbusHandler = modbusHandler

        @self.app.route('/load-command', methods=['POST', 'GET'])
        def loadCommand() :
            if request.method == 'POST':
                try :
                    data = request.json
                    slaveId = data['slave_id']
                    value = data['load_command']
                    message = ModbusMessage(slaveId, "load_command", value)
                    self.modbusHandler.putToQueue(message)
                    
                    response = {
                        "code": "200",
                        "msg": "SEND_SUCCESS",
                        "status": True
                    }
                    return make_response(response, 200)
                except :
                    response = {
                        "code": "400",
                        "msg": "BAD_REQUEST",
                        "status": False
                    }
                    return make_response(response, 400)
                
        @self.app.route('/load-mode', methods=['POST', 'GET'])
        def loadMode() :
            if request.method == 'POST':
                try :
                    data = request.json
                    slaveId = data['slave_id']
                    value = data['load_mode']
                    message = ModbusMessage(slaveId, "load_mode", value)
                    self.modbusHandler.putToQueue(message)
                    
                    response = {
                        "code": "200",
                        "msg": "SEND_SUCCESS",
                        "status": True
                    }
                    return make_response(response, 200)
                except :
                    response = {
                        "code": "400",
                        "msg": "BAD_REQUEST",
                        "status": False
                    }
                    return make_response(response, 400)
            
        
        @self.app.route('/get-info')
        def serveData() :
            response = {
                "info" : self.data.getInfo()
            }
            return response
        
        # @self.app.get('/get-param')
        # def getParam() :
        #     lowVoltage : dict = {
        #         "other" : self.data.lowVoltageOther,
        #         "bts" : self.data.lowVoltageBts,
        #         "vsat" : self.data.lowVoltageVsat
        #     }
        #     reconnectVoltage : dict = {
        #         "other" : self.data.reconnectVoltageOther,
        #         "bts" : self.data.reconnectVoltageBts,
        #         "vsat" : self.data.reconnectVoltageVsat
        #     }
        #     response = {
        #         "low_voltage" : lowVoltage,
        #         "reconnect_voltage" : reconnectVoltage
        #     }
        #     return response
        
        @self.app.route('/get-setting')
        def getSetting() :
            response = {
                "setting" : self.data.getSetting()
            }
            return response

    def run(self) :
        self.app.run(host='0.0.0.0', port=8001)
    