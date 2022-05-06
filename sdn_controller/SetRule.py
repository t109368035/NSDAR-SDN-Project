import re
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.NodeTable import NodeTable
from DBControll.UserTable import UserTable
from DBControll.RuleTable import RuleTable
from sdn_controller.rest_api_command import PostRestAPI
#from urllib import response
import requests

class SetRule:
    def __init__(self):
        ConnectDatabase()

    def post_request(self, user_ip=None, rule_list=None, action='add'):
        url = "http://localhost:8080/stats/flowentry/"+action
        headers = {'Content-Type': 'text/plain'}
        if action == 'add':
            self.add_rule(url, headers, user_ip, rule_list)
        else:
            self.delete_rule(url, headers)
        '''for rule in rule_list:
            response = requests.request("POST", url, headers=headers, data=rule)
            if action == 'add':
                RuleTable().insert_a_rule(user_ip, rule, self.add_rule(response))    
            else:
                print('{}\n{}'.format(self.delete_rule(response), rule))'''
        #print(RuleTable().pop_user_rule(user_ip))
    
    def delete_rule(self, url, headers):
        for ip in UserTable().pop_all_user():
            for rule in RuleTable().pop_user_rule(ip):
                requests.request("POST", url, headers=headers, data=rule)
            RuleTable().delete_user_rule(ip)
            UserTable().delete_user(ip)

    def add_rule(self, url, headers, user_ip, rule_list):
        for rule in rule_list:
            response = requests.request("POST", url, headers=headers, data=rule)
            if '200' in str(response):
                status = 'Add Success'
            else:
                status = 'Add Fail'
            RuleTable().insert_a_rule(user_ip, rule, status)

    '''def add_rule(self, response):        
        if '200' in str(response):
            return 'Add Success'
        else:
            return 'Add Fail' '''

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
                rule = rule + PostRestAPI(user_info=user_info, node_info=NodeTable().pop_node_info(node), next_node_info=NodeTable().pop_node_info(path[node_index+1]), previous_node_info=None, port=port).map()
                
            elif node_index == len(path)-1:
                rule = rule + PostRestAPI(user_info=user_info, node_info=NodeTable().pop_node_info(node), next_node_info=None, previous_node_info=NodeTable().pop_node_info(path[node_index-1]), port=None).mpp()
            else:
                port_list = ['"IN_PORT"', '"IN_PORT"']
                c_node = int(re.search('\d+$',path[node_index]).group())
                n_node = int(re.search('\d+$',path[node_index+1]).group())
                p_node = int(re.search('\d+$',path[node_index-1]).group())
                if abs(c_node - p_node) == 1 and abs(n_node - c_node) != 1: #[next, previous]
                    port_list = [1, 2]
                if abs(c_node - p_node) != 1 and abs(n_node - c_node) == 1:
                    port_list = [2, 1]
                rule = rule + PostRestAPI(user_info=user_info, node_info=NodeTable().pop_node_info(node), next_node_info=NodeTable().pop_node_info(path[node_index+1]), previous_node_info=NodeTable().pop_node_info(path[node_index-1]), port=port_list).mp()

        #print(rule)
        self.post_request(user_ip=user_info['user_ip'], rule_list=rule)