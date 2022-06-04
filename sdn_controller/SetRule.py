import re
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.NodeTable import NodeTable
from DBControll.UserTable import UserTable
from DBControll.RuleTable import RuleTable
from sdn_controller.rest_api_command import PostRestAPI
import requests

class SetRule:
    def __init__(self):
        ConnectDatabase()

    def post_request(self, rule,  action):
        url = "http://localhost:8080/stats/flowentry/"+action
        headers = {'Content-Type': 'text/plain'}
        response = requests.request("POST", url, headers=headers, data=rule)
        return str(response)
    
    def delete_rule(self, action='all', ip=None):
        if action == 'all':
            for ip in UserTable().pop_all_user():
                for rule in RuleTable().pop_user_rule(ip):
                    print('Delete {}, {}'.format(self.check_status(self.post_request(rule, 'delete')), rule))
                RuleTable().delete_user_rule(ip)
                UserTable().delete_user(ip)
        if action == 'single user':
            for rule in RuleTable().pop_user_rule(ip):
                print('Delete {}, {}'.format(self.check_status(self.post_request(rule, 'delete')), rule))
            RuleTable().delete_user_rule(ip)
            UserTable().delete_user(ip)

    def add_rule(self, user_ip, rule_list):
        for rule in rule_list:
            status = self.check_status(self.post_request(rule, 'add'))
            RuleTable().insert_a_rule(user_ip, rule, status)
    
    def check_status(self, status):
        if '200' in status:
            return 'Success'
        else:
            return 'Fail'

    def excute(self,ip_address):
        rule = list()
        user_info = UserTable().pop_user_info(ip_address)
        path = eval(user_info['user_path'])
        """*index是頭=>map, index是中間=>mp, index是尾=>mpp
           *利用node ip來判別input, output port"""
        for node in path:
            node_index = path.index(node)
            if node_index == 0:
                c_node = int(re.search('\d+$',path[node_index]).group())
                n_node = int(re.search('\d+$',path[node_index+1]).group())
                if abs(n_node - c_node) == 1:
                    port = 2
                else:
                    port = 1
                rule = rule + PostRestAPI(user_info=user_info, node_info=NodeTable().pop_node_info(node),
                                          next_node_info=NodeTable().pop_node_info(path[node_index+1]),
                                          previous_node_info=None, port=port).map()  
            elif node_index == len(path)-1:
                rule = rule + PostRestAPI(user_info=user_info, node_info=NodeTable().pop_node_info(node),
                                          next_node_info=None,
                                          previous_node_info=NodeTable().pop_node_info(path[node_index-1]),
                                          port=None).mpp()
            else:
                port_list = ['"IN_PORT"', '"IN_PORT"']
                c_node = int(re.search('\d+$',path[node_index]).group())
                n_node = int(re.search('\d+$',path[node_index+1]).group())
                p_node = int(re.search('\d+$',path[node_index-1]).group())
                if abs(c_node - p_node) == 1 and abs(n_node - c_node) != 1: #[next, previous]
                    port_list = [1, 2]
                if abs(c_node - p_node) != 1 and abs(n_node - c_node) == 1:
                    port_list = [2, 1]
                rule = rule + PostRestAPI(user_info=user_info, node_info=NodeTable().pop_node_info(node),
                                          next_node_info=NodeTable().pop_node_info(path[node_index+1]),
                                          previous_node_info=NodeTable().pop_node_info(path[node_index-1]),
                                          port=port_list).mp()

        self.add_rule(user_ip=user_info['user_ip'], rule_list=rule)