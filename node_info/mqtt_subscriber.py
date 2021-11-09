import paho.mqtt.client as mqtt
import json
from PyQt5.QtCore import QThread,pyqtSignal
from node_info.etx_check_and_format import change_format, check_etx

'''
蒐集各個節點的etx
'''
class MQTT_Subscriber(QThread):
    # map15_user = pyqtSignal(dict)
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.client = mqtt.Client()
        self.send_etx_to_alg_flag = True
        self.collect_etx_member = list()
        self.collect_etx_value = dict()
        
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe('etx_infomation')

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        etx_infomation = json.loads(msg.payload)
        #print(etx_infomation)
        self.etx_data_process(etx_infomation)


    def etx_data_process(self, etx_infomation):
        check_etx(self.collect_etx_member, self.collect_etx_value, etx_infomation)
        print(self.collect_etx_member)
        print(self.collect_etx_value)
        if len(self.collect_etx_member) == 4: # => 要想個自動化的方法來設定etx數量
            print(change_format(self.collect_etx_value))
        

    def serve(self):
        self.start()

    def run(self):
        self.get()

    def get(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect("192.168.1.143", 1883, 60)

        self.client.loop_forever()

if __name__ == '__main__':
    CollectionETX = MQTT_Subscriber()
    CollectionETX.get()
