import subprocess, time
from PyQt5.QtCore import QThread,pyqtSignal
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.AppTable import AppTable

'''
擷取在map的live flow
'''
class Get_Live_Flow(QThread):
    def __init__(self, vlan=None, ip=None):
        super().__init__()
        self.vlan = vlan
        self.ip = ip
        ConnectDatabase()
    
    def run(self):
        if self.vlan:
            self.get()

    def check_access_node(self):
        if int(self.vlan) <= 150:
            return '15' #map15

    def get_row_data(self):        
        #####取的live flow
        cmd = 'curl -u admin:eelab210 "http://192.168.1.{}:3000/lua/rest/v2/get/flow/active.lua?ifid=5"'.format(self.check_access_node())
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        raw_data, err = p.communicate()
        raw_data = raw_data.decode('utf-8')
        raw_data = raw_data.replace('true','"true"')
        raw_data = raw_data.replace('false','"false"')
        dict_data = eval(raw_data)
        all_live_flow = dict_data['rsp']['data']
        return all_live_flow
        #print(all_live_flow)

    def get(self):
        #####將單一使用者的和其使用的APP製作成字典
        #print('before delay{}: {}'.format(self.vlan,time.ctime()))
        time.sleep(20)
        #print('after delay{}: {}'.format(self.vlan, time.ctime()))
        user_ip = self.ip
        app_dict = dict()
        app_dict[user_ip] = dict()
        for flow in self.get_row_data():
            client_ip = flow['client']['ip']
            client_app = flow['protocol']['l7']
            server_ip = flow['server']['ip']
            if user_ip == client_ip and server_ip != '10.10.2.1' and 'DNS' not in client_app and 'DHCP' not in client_app and 'SSDP' not in client_app:
                #print("==========\n{}\n==========\n".format(flow))
                app_dict[user_ip][client_app] = set()
                app_dict[user_ip][client_app].add(server_ip)
        print(app_dict)
        #print('\n\n\n')

        #####將使用者使用APP以及其ip列出
        AppTable().delete_user_app(user_ip)
        if app_dict[user_ip]:
            #print(user_ip)
            for app, ip in app_dict[user_ip].items():
                #print('{}: {}'.format(app, list(ip)))
                AppTable().insert_a_app(user_ip, app, ','.join(list(ip)))   
            #print('\n')

if __name__ == '__main__':
    capture = Get_Live_Flow('107', '10.10.2.107')
    capture.get()