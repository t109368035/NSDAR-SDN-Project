import paho.mqtt.client as mqtt
import json, time, threading
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.NodeTable import NodeTable

MQTT_BROKER = '192.168.1.143'
MQTT_PORT = 1883
MQTT_ALIVE = 60

class MQTT(QThread):
    dpid_info = pyqtSignal(str)
    iw_info_d = pyqtSignal(dict)
    def __init__(self,parent):
        super().__init__(parent)
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_ALIVE)
        self.client.on_connect = self.on_connect
        self.dpid_dict = dict()
        self.dpid_flag = True
        self.iw_dict = dict()
        self.dpid_timer = QTimer(self)
        self.dpid_timer.timeout.connect(self.dpid)
        self.dpid_timer.start(2000)
        self.iw_timer = QTimer(self)
        self.iw_timer.timeout.connect(self.iw_info)
        self.iw_timer.start(2000)
        ConnectDatabase()

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("Connected with result code "+str(rc))
        self.client.subscribe('node_info')

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)
        #print(data)
        if data.get('dpidinfo'):
            node_ID = list(data['dpidinfo'].keys())[0]
            node_list = NodeTable().pop_all_node()
            if node_ID not in node_list:
                node_info = data['dpidinfo'][node_ID]
                NodeTable().insert_node(node_name=node_ID, node_dpid=node_info['dpid'], node_mac=node_info['mac'])
                self.dpid_info.emit('add node')    
            """
            nodetodpid = data['dpidinfo']
            node_ID = list(nodetodpid.keys())[0]
            if node_ID not in self.dpid_dict:
                self.dpid_dict.update(nodetodpid)
                if len(self.dpid_dict) == 3:
                    print(self.dpid_dict)
                    self.dpid_flag = False
                    self.dpid_info.emit(self.dpid_dict)
            """
        elif data.get('iwinfo'):
            pathiw = data['iwinfo']
            path_ID = list(pathiw.keys())
            for key in path_ID:
                #signal = float(pathiw[key]['signal'])
                #tx_bitrate = float(pathiw[key]['tx_bitrate'])
                self.iw_dict[key] = pathiw[key]
                if len(self.iw_dict) == len(NodeTable().pop_all_node()):
                    #print('signal:{}, tx bitrate:{}'.format(signal, tx_bitrate))
                    #print(self.iw_dict)
                    self.iw_info_d.emit(self.iw_dict)
                    self.iw_dict = dict()

    def subscribe(self):
        self.client.on_message = self.on_message
        self.client.loop_forever()
    
    def publish(self, topic, parameters):
        data = json.dumps(parameters)
        self.client.publish(topic, data)
    
    def dpid(self):
        if self.dpid_flag:
            self.publish('info_request', 'dpidrequest')
        
    def iw_info(self):
        self.publish('info_request', 'iwrequest')

    def serve(self):
        self.start()

    def run(self):
        sub = threading.Thread(target=self.subscribe, daemon=True)
        #pub_dpid = threading.Thread(target=self.dpid, daemon=True)
        #pub_iwinfo = threading.Thread(target=self.iw_info, daemon=True)
        sub.start()
        #pub_dpid.start()
        #pub_iwinfo.start()
        #while True:
        #    command = input()
        #    if command == "finish":
        #        break
        #print("leaving ....... ")

if __name__ == '__main__':
    nodeinfo = MQTT()
    nodeinfo.run()

    
