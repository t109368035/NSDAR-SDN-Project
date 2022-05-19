from ssh_center import sshCenter

class annoy_test():
    def __init__(self):
        self.sshcenter = sshCenter()

    def excute(self):
        try:
            bandwidth = self.sshcenter.send_command(ip='192.168.1.15', command='python3 /home/pi/Desktop/iperf_for_annoy.py')
            print(bandwidth)
        except:
            pass
if __name__ == '__main__':
    reboot = annoy_test()
    reboot.excute()