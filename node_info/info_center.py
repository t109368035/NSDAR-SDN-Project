#尚未完成收到節點資訊後，處理的程序。
import paho.mqtt.client as mqtt
import json, re
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.NodeTable import NodeTable
from DBControll.LinkTable import LinkTable
from DBControll.PathTable import PathTable
from path_calculate.dikstra_graph import Graph

MQTT_BROKER = '192.168.1.143'
MQTT_PORT = 1883
MQTT_ALIVE = 60

class NodeINFO(QThread):
    dpid_info = pyqtSignal(str)
    start_getpacket15 = pyqtSignal(str)
    start_getpacket05 = pyqtSignal(str)
    enable_ETT = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        ConnectDatabase()
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_ALIVE)
        self.client.on_connect = self.on_connect
        self.dpid_timer = QTimer(self)
        self.dpid_timer.timeout.connect(self.dpid)
        self.dpid_timer.start(2000)
        self.ett_list = list()
        self.getpacket_flag = False
        self.link_count = 0
        
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("Connected with result code "+str(rc))
        self.client.subscribe('node_info')

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)
        if data.get('dpidinfo'):
            self.add_node(data)
        elif data.get('chquality'):
            print(data)
            self.add_link(data['chquality'])

    def subscribe(self):
        self.client.on_message = self.on_message
        self.client.loop_forever()
    
    def publish(self, topic, parameters):
        data = json.dumps(parameters)
        self.client.publish(topic, data)

    def dpid(self):
        if len(NodeTable().pop_all_node()) == 12 and self.getpacket_flag is False:
            self.getpacket_flag = True
            self.enable_ETT.emit('True')
            #self.start_getpacket15.emit('start')
            #self.start_getpacket05.emit('start')
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

    def add_link(self, data):
        self.link_count+=1
        LinkTable().insert_link(start_node=data['start'], end_node=data['end'],
                                bandwidth=data['bandwidth'], ETX=data['etx'])#bandwidth需要除役以2嗎?因為會掉包
        if self.link_count == 12:
            self.get_APP_path()
            self.get_normal_path()
            self.link_count = 0

    def get_normal_path(self):
        for AP in ['map15', 'map5']:
            btype = 'normal'
            graph = Graph(LinkTable().pop_ETT())
            path = graph.dijkstra(AP, 'out')
            print('start from {}, type is {}\n{}\n\n'.format(AP, 'normal', path))
            PathTable().insert_path(AP=AP.replace('\'','"'), app_type=btype.replace('\'','"'), path=str(path).replace('\'','"'))

    def get_APP_path(self):
        for btype in ['Mission', 'Mobile', 'Massive']:
            for AP in ['map15', 'map5']:
                graph = Graph(LinkTable().pop_ETT())
                path = graph.dijkstra(AP, 'out')
                self.minus_use_bandwidth(path, btype)
                print('start from {}, type is {}\n{}\n\n'.format(AP, btype, path))
                PathTable().insert_path(AP=AP.replace('\'','"'), app_type=btype.replace('\'','"'), path=str(path).replace('\'','"'))

    def minus_use_bandwidth(self,path,btype):
        for i in range(0,len(path)-1): #拿出目前節點以及下一個節點
            c_node = int(re.search('\d+$',path[i]).group())
            n_node = int(re.search('\d+$',path[i+1]).group())
            if not abs(n_node - c_node) == 1: #取出無線link
                for link in self.get_link_have_minus(path[i], path[i+1]): #取出受到影響所有link                    
                        original_bandwidth = LinkTable().pop_bandwidth(start_node=link[0], end_node=link[1])
                        bandwidth=original_bandwidth-self.get_btype_bandwidth(btype)
                        if bandwidth<=0:
                            LinkTable().delete_link(start_node=link[0],end_node=link[1])
                        else:
                            LinkTable().modify_bandwidth(start_node=link[0], end_node=link[1], bandwidth=bandwidth)
    
    def get_link_have_minus(self, c_node, n_node):
        all_link = LinkTable().pop_link_end_with(end_node=c_node) + LinkTable().pop_link_start_with(start_node=c_node) + LinkTable().pop_link_end_with(end_node=n_node) + LinkTable().pop_link_start_with(start_node=n_node)
        all_link.remove([c_node,n_node])
        print(all_link)
        return all_link

    def get_btype_bandwidth(self, btype):
        if btype is 'Mission':#設定每種應用類型使用的頻寬
            use = 25000000
        elif btype is 'Mobile':
            use = 15000000
        elif btype is 'Massive':
            use = 5000000
        return use

    def run(self):
        self.subscribe()
    
if __name__ == '__main__':
    nodeinfo = NodeINFO()
    nodeinfo.run()

    
