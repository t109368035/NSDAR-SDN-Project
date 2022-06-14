from ssh.ssh_center import sshCenter
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.NodeTable import NodeTable
import time

class PowerControll():
    def __init__(self):
        self.sshcenter = sshCenter()
        ConnectDatabase()

    def node_reboot(self, node):
        try:
            if node == 'map15':
                self.sshcenter.send_command(ip='192.168.1.15', command='sudo reboot')
                time.sleep(5)
            return node
        except:
            self.node_reboot(node)
