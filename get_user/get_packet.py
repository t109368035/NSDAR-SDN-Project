import pyshark
import re
from PyQt5.QtCore import QThread, pyqtSignal
from ssh.ssh_center import sshCenter
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.UserTable import UserTable
from sdn_controller.SetRule import SetRule

'''
capture remote
抓取map網卡之arp封包
'''
class Remote_capture(QThread):
    map_user = pyqtSignal(str)
    def __init__(self, node=None):
        super().__init__()
        self.sshcenter = sshCenter()
        self.node = node
        ConnectDatabase()

    def run(self):
        self.get()

    def get(self):
        try:
            capture = pyshark.RemoteCapture('192.168.1.{}'.format(self.node), 'eth0', bpf_filter='ip src host 10.10.2')
            for packet in capture: #逐一取出擷取到的封包並且存到database
                self.add_user(packet['IP'].src, packet['ETH'].src)
        except:
            self.get()

    def add_user(self, ip, mac):
        if ip not in UserTable().pop_all_user() and ip != '10.10.2.1' and '10.10.2' in ip:
            vlan = re.search('\d+$',ip).group()
            if int(vlan) <= 150:
                AP = 'map15'
                path = ['map15','map16','mp46','mpp99']
            else:
                AP = 'map5'
                path = ['map5','mp45','mpp88']
            UserTable().insert_a_user(user_ip=ip, user_mac=mac, user_vlan=vlan,
                                      user_path=str(path).replace('\'','"'),
                                      user_type='innitial', user_ap=AP)
            SetRule().excute(ip_address=ip)
            try:
                for i in ['192.168.1.98', '192.168.1.99', '192.168.1.88', '192.168.1.89']:
                    self.sshcenter.send_command(ip=i, command='sudo arp -s {} {} -i ovsbr'.format(ip, mac))
            except Exception as e:
                print('######get_packet->ssh######\n{}\n######get_packet->ssh######'.format(e))
            self.map_user.emit('map{} start'.format(self.node))
        
if __name__ == '__main__':
    RemoteCapture = Remote_capture()
    RemoteCapture.get()
