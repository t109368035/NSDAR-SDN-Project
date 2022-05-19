from paramiko import SSHClient, AutoAddPolicy

class sshCenter():
    def __init__(self):
        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())


    def send_command(self, ip, command):
        self.ssh_client.connect(hostname=ip, username='pi', password='raspberry')
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        out = stdout.read().decode().strip()
        self.ssh_client.close()
        return out

if __name__ == '__main__':
    c = sshCenter()
    c.send_command('192.168.1.15','sudo ifconfig eth0 down')
