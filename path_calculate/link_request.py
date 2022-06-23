import json, time
import paho.mqtt.client as mqtt
from PyQt5.QtCore import QThread, pyqtSignal

MQTT_BROKER = '192.168.1.143'
MQTT_PORT = 1883
MQTT_ALIVE = 60

class LinkRequest(QThread):
    enable_ETT = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_ALIVE)

    def publish(self, topic, parameters):
        data = json.dumps(parameters)
        self.client.publish(topic, data)

    def run(self):
        for i in range(1,13):
            self.publish('info_request', 'test{}'.format(i))
            time.sleep(4)
        self.enable_ETT.emit('True')
        print("link collect already done.")
