from ssh_center import sshCenter

class REBOOT():
    def __init__(self):
        self.sshcenter = sshCenter()

    def excute(self):
        for i in ['192.168.1.98', '192.168.1.15', '192.168.1.55', '192.168.1.16', '192.168.1.56', '192.168.1.99']:
            try:
                #self.sshcenter.send_command(ip=i, command='sudo ovs-ofctl -O openflow13 del-flows ovsbr')
                self.sshcenter.send_command(ip=i, command='sudo reboot')
            except:
                pass
if __name__ == '__main__':
    reboot = REBOOT()
    reboot.excute()