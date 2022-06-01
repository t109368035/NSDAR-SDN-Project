import pyshark
import re, time
from threading import Thread
from PyQt5.QtCore import QThread,pyqtSignal, QTimer, Qt
from get_user.get_flow import Get_Live_Flow
from ssh.ssh_center import sshCenter
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.UserTable import UserTable
from sdn_controller.SetRule import SetRule

'''
capture remote
抓取map網卡之arp封包
'''
class Remote_capture(QThread):
    map15_user = pyqtSignal(str)
    def __init__(self,parent):
        super().__init__(parent)
        self.capture = None
        self.parent = parent
        self.user_data = dict()
        self.sshcenter = sshCenter()
        self.capture_node_15 = '15'
        #self.get15_timer = QTimer(self)
        #self.get15_timer.timeout.connect(self.get)
        #self.get15_timer.start(2000)
        ConnectDatabase()

    def serve(self):
        self.start()

    def run(self):
        #self.get15_timer.start(20000)
        #print('hello')
        #get_15 = Thread(target=self.get, daemon=True)
        #get_15.start()
        self.get()

    def get(self):
        print("get user data: {}".format(time.ctime()))
        #while True:
        self.capture = pyshark.RemoteCapture('192.168.1.{}'.format(self.capture_node_15), 'eth2', bpf_filter='ip src host 10.10.2')
        self.capture.sniff(packet_count=60)
        #self.capture.sniff(timeout=10)
        self.capture.close()
        #packet_quantity = re.search('[0-9]+', str(self.capture)).group() #查看數量
        for packet in self.capture.sniff_continuously(packet_count=60): #逐一取出擷取到的封包並且存到database
            ip = packet['IP'].src
            mac = packet['ETH'].src
            if ip not in UserTable().pop_all_user() and ip != '10.10.2.1' and '10.10.2' in ip:
                vlan = re.search('\d+$',ip).group()
                UserTable().insert_a_user(user_ip=ip, user_mac=mac, user_vlan=vlan, user_path=str(['map15','mp55','mpp98']).replace('\'','"'), user_type='innitial')
                self.map15_user.emit('add user')
                SetRule().excute(ip_address=ip)
                try:
                    for i in ['192.168.1.98', '192.168.1.99']:
                        self.sshcenter.send_command(ip=i, command='sudo arp -s {} {} -i ovsbr'.format(ip, mac))
                    #self.new_user(ip, vlan)
                except Exception as e:
                    print('######get_packet->ssh######')
                    print(e)
                    print('######get_packet->ssh######')
        print("get user data defore delay: {}".format(time.ctime()))
        #self.timedelay(0)
        time.sleep(3)
        print("get user data after delay: {}".format(time.ctime()))
        self.restart_get(self.capture_node_15)

    def restart_get(self, node):
        if node == '15':
            self.get()
    
    def timedelay(self,i):
        i+=1
        if i < 10:
            print("\n========\ndelay{}: {}\n========\n".format(i, time.ctime()))
            # run again after 500ms with argument
            QTimer.singleShot(5000, self.timedelay(i))

    def new_user(self, ip, vlan):##計算時間? 並重新安排路徑    
        Thread(target=self.get_flow,
                         kwargs={
                            'ip': ip,
                            'vlan': vlan}, daemon=True).start()
        
    def get_flow(self, ip, vlan):
        time.sleep(10)
        Get_Live_Flow(vlan, ip).get()
        
if __name__ == '__main__':
    RemoteCapture = Remote_capture()
    RemoteCapture.get()