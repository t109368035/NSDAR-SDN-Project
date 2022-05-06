import pyshark
import re, time, threading
from PyQt5.QtCore import QThread,pyqtSignal, QTimer, Qt
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
        ConnectDatabase()
        #self.cap_timer = QTimer(self)
        #self.cap_timer.timeout.connect(self.threadofget)
        #self.cap_timer.start(10000)

    def serve(self):
        self.start()

    def run(self):
        self.get()
        #print("start get user data")

    def threadofget(self):
        sub = threading.Thread(target=self.get)
        sub.start()
        sub.join()
        
    def get(self):
        #while True:
        self.capture = pyshark.RemoteCapture('192.168.1.15', 'eth2', bpf_filter='ip src host 10.10.2')
        self.capture.sniff(packet_count=60)
        self.capture.close()
        #packet_quantity = re.search('[0-9]+', str(self.capture)).group() #查看數量

        for packet in self.capture.sniff_continuously(packet_count=60): #逐一取出擷取到的封包並且存到database
            ip = packet['IP'].src
            mac = packet['ETH'].src
            if ip not in UserTable().pop_all_user() and ip != '10.10.2.1' and '10.10.2' in ip:
                UserTable().insert_a_user(user_ip=ip, user_mac=mac, user_vlan=re.search('\d+$',ip).group(), user_path=str(['map15','mp55','mpp98']).replace('\'','"'), user_type='innitial')
                self.map15_user.emit('add user')
                SetRule().excute(ip_address=ip)
                try:
                    for i in ['192.168.1.98', '192.168.1.99']:
                        self.sshcenter.send_command(ip=i, command='sudo arp -s {} {} -i ovsbr'.format(ip, mac))
                except Exception as e:
                    print('######get_packet->ssh######')
                    print(e)
                    print('######get_packet->ssh######')
        time.sleep(10)
        QTimer.singleShot(0, self.get())

if __name__ == '__main__':
    RemoteCapture = Remote_capture()
    RemoteCapture.get()
    
    ##此方法失敗
    #timer = QTimer()
    #timer.timeout.connect(RemoteCapture.get())
    #timer.setInterval(10000)
    #timer.start()
    