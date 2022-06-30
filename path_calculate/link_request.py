import json, time
import paho.mqtt.client as mqtt
from PyQt5.QtCore import QThread, pyqtSignal
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.RuleTable import RuleTable

MQTT_BROKER = '192.168.1.143'
MQTT_PORT = 1883
MQTT_ALIVE = 60

class LinkRequest(QThread):
    enable_ETT = pyqtSignal(str)
    refresh_rule = pyqtSignal(str)
    start_getpacket15 = pyqtSignal(str)
    start_getpacket05 = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        ConnectDatabase()
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_ALIVE)

    def publish(self, topic, parameters):
        data = json.dumps(parameters)
        self.client.publish(topic, data)

    def run(self):
        for i in reversed(range(1,13)):
            self.publish('info_request', 'test{}'.format(i))
            time.sleep(4)
        print("link collect already done.")
        self.enable_ETT.emit('True')
        if RuleTable().pop_all_rule() != list():
            self.refresh_rule.emit('refresh')
        else:
            print("未進入refresh_normal_rule")
        self.start_getpacket15.emit('start')
        self.start_getpacket05.emit('start')
