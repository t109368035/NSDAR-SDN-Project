#尚未完成收到節點資訊後，處理的程序。
import paho.mqtt.client as mqtt
import json, time, threading
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.NodeTable import NodeTable
from path_calculate.dikstra_graph import Graph

MQTT_BROKER = '192.168.1.143'
MQTT_PORT = 1883
MQTT_ALIVE = 60

class MQTT(QThread):
    dpid_info = pyqtSignal(str)
    start_getpacket15 = pyqtSignal(str)
    start_getpacket05 = pyqtSignal(str)
    enable_ETT = pyqtSignal(str)
    #node_fail = pyqtSignal(str)
    def __init__(self,parent):
        super().__init__(parent)
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_ALIVE)
        self.client.on_connect = self.on_connect
        self.dpid_timer = QTimer(self)
        self.dpid_timer.timeout.connect(self.dpid)
        self.dpid_timer.start(2000)
        self.etx_list = list()
        self.getpacket_flag = False
        ConnectDatabase()

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("Connected with result code "+str(rc))
        self.client.subscribe('node_info')

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)
        if data.get('dpidinfo'):
            self.add_node(data)
        elif data.get('chquality'):
            print(data)
            self.collect_ett(data)
        #elif data.get('fail'):
        #    self.node_fail.emit(data['fail'])
        #    NodeTable().delete_user(data['fail'])
        #    self.getpacket_flag = False

    def subscribe(self):
        self.client.on_message = self.on_message
        self.client.loop_forever()
    
    def publish(self, topic, parameters):
        data = json.dumps(parameters)
        self.client.publish(topic, data)

    def dpid(self):
        if len(NodeTable().pop_all_node()) == 12 and self.getpacket_flag is False:
            self.getpacket_flag = True
            self.enable_ETT.emit('add node')
            self.start_getpacket15.emit('start')
            self.start_getpacket05.emit('start')
            self.dpid_timer.stop()
        elif len(NodeTable().pop_all_node()) < 12 and self.getpacket_flag is True:
            self.getpacket_flag = False
        else:
            self.publish('info_request', 'dpidrequest')

    def add_node(self, data):
        node_ID = list(data['dpidinfo'].keys())[0]
        node_list = NodeTable().pop_all_node()
        if node_ID not in node_list:
            node_info = data['dpidinfo'][node_ID]
            NodeTable().insert_node(node_name=node_ID, node_dpid=node_info['dpid'], node_mac=node_info['mac'])
            self.dpid_info.emit('add node')

    def collect_ett(self, data):
        packetsize = 12112 #bits
        bandwidth = data['chquality']['bandwidth']
        if not bandwidth or bandwidth == 0.0:
            bandwidth = 1000
        etx = data['chquality']['etx']
        ett = data['chquality']['start'], data['chquality']['end'],  etx*(packetsize/bandwidth)
        print(type(ett))
        print(ett)
        self.etx_list.append(ett)
        #if len(self.etx_list) == :
        #    path = Graph(self.etx_list)
        #    print(list(path.dijkstra("map15", "out")))

    def run(self):
        self.subscribe()
    
if __name__ == '__main__':
    nodeinfo = MQTT()
    nodeinfo.run()

    
