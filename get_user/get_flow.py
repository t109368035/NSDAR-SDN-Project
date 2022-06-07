import subprocess, time
from PyQt5.QtCore import QThread, pyqtSignal
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.AppTable import AppTable
from DBControll.UserTable import UserTable

'''
擷取在map的live flow
'''
class Get_Live_Flow(QThread):
    user_table_fresh = pyqtSignal(list)
    stop_getflow = pyqtSignal(str)
    def __init__(self, node):
        super().__init__()
        self.node = node
        ConnectDatabase()
    
    def run(self):
        self.store_user_flow()

    def row_data_proccess(self, raw_data):
        raw_data = raw_data.decode('utf-8')
        raw_data = raw_data.replace('true','"true"')
        raw_data = raw_data.replace('false','"false"')
        dict_data = eval(raw_data)
        all_live_flow = dict_data['rsp']['data']
        return all_live_flow

    def get_row_data(self):        
        #####get live flow
        try:
            cmd = 'curl -u admin:eelab210 "http://192.168.1.1{}:3000/lua/rest/v2/get/flow/active.lua?ifid=2"'.format(self.node)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            raw_data, err = p.communicate()
            return self.row_data_proccess(raw_data)
        except:
            return None

    def store_user_flow(self):
        time.sleep(20)
        store_time = time.ctime()
        user_list = UserTable().pop_all_user()
        flow_list = self.get_row_data()
        check_user_list = set()
        if user_list is not None and flow_list is not None:
            for user in user_list:
                for flow in flow_list:
                    client_ip = flow['client']['ip']
                    if user == client_ip and 'DNS' not in flow['protocol']['l7']:
                        AppTable().insert_a_app(store_time, user, flow['client']['is_dhcp'],flow['client']['port'],
                                                flow['server']['name'],flow['server']['ip'],flow['server']['port'],
                                                flow['server']['is_broadcast'],flow['protocol']['l4'], 
                                                flow['protocol']['l7'], flow['first_seen'], flow['last_seen'],
                                                flow['duration'], flow['bytes'])
                        check_user_list.add(user)
            self.delete_user(user_list, check_user_list)
            self.restart_store()
        elif user_list is None:
            self.stop_getflow.emit('map{} stop'.format(self.node))
    
    def restart_store(self):
        self.store_user_flow()

    def delete_user(self, original_user_list, check_user_list):
        delete_user = list()
        for user in original_user_list:
            if user not in check_user_list:
                delete_user.append(user)
        if delete_user:
            self.user_table_fresh.emit(delete_user)