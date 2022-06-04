import subprocess, time
from PyQt5.QtCore import QThread,pyqtSignal
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.AppTable import AppTable
from DBControll.UserTable import UserTable

'''
擷取在map的live flow
'''
class Get_Live_Flow(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        ConnectDatabase()
    
    def run(self):
        self.restart_store()

    def row_data_proccess(self, raw_data):
        raw_data = raw_data.decode('utf-8')
        raw_data = raw_data.replace('true','"true"')
        raw_data = raw_data.replace('false','"false"')
        dict_data = eval(raw_data)
        all_live_flow = dict_data['rsp']['data']
        return all_live_flow

    def get_row_data(self):        
        #####get live flow
        cmd = 'curl -u admin:eelab210 "http://192.168.1.15:3000/lua/rest/v2/get/flow/active.lua?ifid=5"'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        raw_data, err = p.communicate()
        return self.row_data_proccess(raw_data)

    def store_user_flow(self):
        store_time = time.ctime()
        app_dict = dict()
        if UserTable().pop_all_user():
            for user in UserTable().pop_all_user():
                app_dict[user] = list()
                for flow in self.get_row_data():
                    client_ip = flow['client']['ip']
                    if user == client_ip and 'DNS' not in flow['protocol']['l7']:
                        AppTable().insert_a_app(store_time, user, flow['client']['is_dhcp'],flow['client']['port'],
                                                flow['server']['name'],flow['server']['ip'],flow['server']['port'],
                                                flow['server']['is_broadcast'],flow['protocol']['l4'], 
                                                flow['protocol']['l7'], flow['first_seen'], flow['last_seen'],
                                                flow['duration'], flow['bytes'])
        self.restart_store()
    
    def restart_store(self):
        time.sleep(20)
        self.store_user_flow()
