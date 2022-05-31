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
    iw_info_d = pyqtSignal(dict)
    def __init__(self,parent):
        super().__init__(parent)
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_ALIVE)
        self.client.on_connect = self.on_connect
        self.dpid_dict = dict()
        self.dpid_flag = True
        self.dpid_timer = QTimer(self)
        self.dpid_timer.timeout.connect(self.dpid)
        self.dpid_timer.start(2000)
        self.etx_list = list()
        #self.iw_dict = dict()
        #self.iw_timer = QTimer(self)
        #self.iw_timer.timeout.connect(self.iw_info)
        #self.iw_timer.start(2000)
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

        elif data.get('chquality'):
            packetsize = 12112 #bits
            bandwidth = data['chquality']['bandwidth']
            etx = data['chquality']['etx']
            ett = data['chquality']['start'], data['chquality']['end'],  etx*(packetsize/bandwidth)
            print(type(ett))
            print(ett)
            #self.etx_list.append(ett)
            #if len(self.etx_list) == 4:
            #    path = Graph(self.etx_list)
            #    print(list(path.dijkstra("map15", "out")))

        elif data.get('iwinfo'):
            pathiw = data['iwinfo']
            path_ID = list(pathiw.keys())
            for key in path_ID:
                self.iw_dict[key] = pathiw[key]
                if len(self.iw_dict) == len(NodeTable().pop_all_node()):
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
        else:
            self.dpid_timer.stop()
        
    def iperf_test_request(self, stage):
        if stage ==  1:
            self.publish('info_request', 'test1')
        elif stage ==2:
            self.publish('info_request', 'test2')

    def iw_info(self):
        self.publish('info_request', 'iwrequest')

    def serve(self):
        self.start()

    def run(self):
        sub = threading.Thread(target=self.subscribe, daemon=True)
        sub.start()
    
        self.iperf_test_request(1)
        time.sleep(3)
        self.iperf_test_request(2)

if __name__ == '__main__':
    nodeinfo = MQTT()
    nodeinfo.run()

    
