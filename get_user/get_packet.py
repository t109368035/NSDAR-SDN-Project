import pyshark
import re
from PyQt5.QtCore import QThread,pyqtSignal


'''
capture remote
抓取map網卡之arp封包
'''
class Remote_capture(QThread):
    map15_user = pyqtSignal(dict)
    def __init__(self,parent):
        super().__init__(parent)
        self.capture = None
        self.parent = parent

    def serve(self):
        self.start()

    def run(self):
        self.get()

    def get(self):
        while True:
            self.capture = pyshark.RemoteCapture('192.168.1.238', 'enp2s0', bpf_filter='arp')
            self.capture.sniff(timeout=10)
            self.capture.close()
            packet_quantity = re.search('[0-9]+', str(self.capture)).group()
            user_data = dict()

            for packet in self.capture.sniff_continuously(packet_count=int(packet_quantity)): #逐一取出擷取到的封包並且製作成dict
                #print('Just arrived:{}'.format(packet))
                if packet.arp.get_field_by_showname('Target IP address') == '10.10.2.1':#確認封包是否是發向10.10.2.1
                    user_data[packet.arp.get_field_by_showname('Sender IP address')] = packet.arp.get_field_by_showname('Sender MAC address')

            print(user_data)
            self.map15_user.emit(user_data)
            self.capture.packets_from_tshark(self.get())


if __name__ == '__main__':
    RemoteCapture = Remote_capture()
    RemoteCapture.get()


