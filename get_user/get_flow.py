import subprocess, time
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.AppTable import AppTable
from DBControll.UserTable import UserTable

'''
擷取在map的live flow
'''
class Get_Live_Flow(QThread):
    user_table_fresh = pyqtSignal(list)
    stop_getflow = pyqtSignal(str)
    node_fail = pyqtSignal(str)
    def __init__(self, node):
        super().__init__()
        self.node = node
        ConnectDatabase()
        self.ftimer = QTimer(self)
        self.ftimer.timeout.connect(self.store_user_flow)
        self.ftimer.start(20000)
    
    def run(self):
        print('\n\n===========\nstart getflow{} : {}\n===========\n\n'.format(self.node, time.ctime()))

    def row_data_proccess(self, raw_data):
        try:
            raw_data = raw_data.decode('utf-8')
            raw_data = raw_data.replace('true','"true"')
            raw_data = raw_data.replace('false','"false"')
            dict_data = eval(raw_data)
        except:
            return None
        if raw_data != '':
            all_live_flow = dict_data['rsp']['data']
            return all_live_flow
        else:
            return None

    def get_row_data(self):        
        #####get live flow
        cmd = 'curl -u admin:eelab210 "http://192.168.1.{}:3000/lua/rest/v2/get/flow/active.lua?ifid=1"'.format(self.node)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        raw_data, err = p.communicate()
        return self.row_data_proccess(raw_data)
  
    def store_user_flow(self):
        store_time = time.ctime()
        user_list = UserTable().pop_AP_user('map{}'.format(self.node))
        #print('user list in dataset: {}'.format(user_list))
        flow_list = self.get_row_data()
        check_user_list = set()
        if user_list and flow_list:
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
            #print('user list in ntop: {}'.format(check_user_list))
            self.delete_user(user_list, check_user_list)
        elif not user_list and flow_list:
            #print('user list is none')
            self.ftimer.stop()
            self.stop_getflow.emit('map{} stop'.format(self.node))
        elif user_list and not flow_list:
            print('\n\n\n==============\nntop出問題了 : {}\n==============\n\n\n'.format(store_time))
            self.ftimer.stop()
            self.stop_getflow.emit('map{} stop'.format(self.node))
            self.node_fail.emit('map{}'.format(self.node))

    def delete_user(self, original_user_list, check_user_list):
        delete_user = list()
        for user in original_user_list:
            if user not in check_user_list:
                delete_user.append(user)
        if delete_user:
            self.user_table_fresh.emit(delete_user)