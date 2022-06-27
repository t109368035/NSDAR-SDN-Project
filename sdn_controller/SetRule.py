import re, time
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.NodeTable import NodeTable
from DBControll.UserTable import UserTable
from DBControll.RuleTable import RuleTable
from DBControll.PathTable import PathTable
from sdn_controller.rest_api_command import GenerateRule
import requests

class SetRule:
    def __init__(self):
        self.rule = None
        self.action = None
        ConnectDatabase()
        self.queue_dict = self.dict_of_queue()

    def post_request(self, rule,  action):
        url = "http://localhost:8080/stats/flowentry/"+action
        headers = {'Content-Type': 'text/plain'}
        response = requests.request("POST", url, headers=headers, data=rule)
        if '200' not in str(response):
            time.sleep(0.3)
            self.post_request(self.rule, self.action)

    def delete_rule(self, action='all', ip=None):
        self.action = 'delete'
        if action == 'all':#改成全刪
            for rule in RuleTable().pop_all_rule():
                self.rule = rule
                self.post_request(rule, 'delete')
            RuleTable().delete_all()
        if action == 'single user':
            for rule in RuleTable().pop_user_rule(ip):
                self.rule = rule
                self.post_request(rule, 'delete')
            RuleTable().delete_user_rule(ip)
            UserTable().delete_user(ip)

    def add_rule(self, ap=None, app_type=None, user_ip=None, rule_list=None, node_name=None, re_add=False):
        self.action = 'add'
        for rule in rule_list:
            self.rule = rule
            self.post_request(rule, 'add')
            if not re_add:
                RuleTable().insert_a_rule(AP=ap, app_type=app_type, user_ip=user_ip, user_rule=rule, node_name=node_name)

    def excute(self,user_ip,ap,app_type,server_ip=None):
        rule = list()
        user_info = UserTable().pop_user_info(user_ip)
        path_info = PathTable().pop_AP_type_path(ap, app_type) 
        vlan = path_info['vlan']
        queue = self.queue_dict[vlan]
        priority = self.assign_priority(app_type)
        path = eval(path_info['path'])
        """
        *index是頭=>map, index是中間=>mp, index是尾=>mpp。
        *利用node ip來判別input, output port。
        *固定的規則只要加一次像是GenerateRule裡面的map_to_node(), mp(), mpp_to_node等function。
        """
        for node in path:
            node_index = path.index(node)
            node_info = NodeTable().pop_node_info(node)
            if node_index == 0:
                c_node = int(re.search('\d+$',path[node_index]).group())
                n_node = int(re.search('\d+$',path[node_index+1]).group())
                if abs(n_node - c_node) == 1:
                    port = 2
                else:
                    port = 1
                rule = GenerateRule(user_info=user_info, node_info=node_info,
                                    next_node_info=NodeTable().pop_node_info(path[node_index+1]),
                                    previous_node_info=None, port=port, vlan=vlan, queue_id=queue, priority=priority, server_ip=server_ip).map()  
                self.add_rule(ap=ap, app_type=app_type, user_ip=user_ip, rule_list=rule, node_name=node_info['node_name'])
                if not RuleTable().pop_AP_type_mp_rule(AP=ap, user_ip='map_for_{}_{}'.format(ap, app_type), node_name=node_info['node_name']):
                    rule = GenerateRule(user_info=user_info, node_info=node_info,
                                    next_node_info=NodeTable().pop_node_info(path[node_index+1]),
                                    previous_node_info=None, port=port, vlan=vlan, queue_id=queue, priority=priority, server_ip=server_ip).map_to_node()  
                    self.add_rule(ap=ap, app_type=app_type, user_ip='map_for_{}_{}'.format(ap, app_type), rule_list=rule, node_name=node_info['node_name'])
            elif node_index == len(path)-1:
                rule = GenerateRule(user_info=user_info, node_info=node_info,
                                    next_node_info=None,
                                    previous_node_info=NodeTable().pop_node_info(path[node_index-1]),
                                    port=None, vlan=vlan, queue_id=queue, priority=priority, server_ip=server_ip).mpp()
                self.add_rule(ap=ap, app_type=app_type, user_ip=user_ip, rule_list=rule, node_name=node_info['node_name'])
                if not RuleTable().pop_AP_type_mp_rule(AP=ap, user_ip='mpp_for_{}_{}'.format(ap, app_type), node_name=node_info['node_name']):
                    rule = GenerateRule(user_info=user_info, node_info=node_info,
                                    next_node_info=None,
                                    previous_node_info=NodeTable().pop_node_info(path[node_index-1]),
                                    port=None, vlan=vlan, queue_id=queue, priority=priority, server_ip=server_ip).mpp_to_node()  
                    self.add_rule(ap=ap, app_type=app_type, user_ip='mpp_for_{}_{}'.format(ap, app_type), rule_list=rule, node_name=node_info['node_name'])
            elif not RuleTable().pop_AP_type_mp_rule(AP=ap, user_ip='mp_for_{}_{}'.format(ap, app_type), node_name=node_info['node_name']):
                port_list = ['"IN_PORT"', '"IN_PORT"']
                c_node = int(re.search('\d+$',path[node_index]).group())
                n_node = int(re.search('\d+$',path[node_index+1]).group())
                p_node = int(re.search('\d+$',path[node_index-1]).group())
                if abs(c_node - p_node) == 1 and abs(n_node - c_node) != 1: #[next, previous]
                    port_list = [1, 2]
                if abs(c_node - p_node) != 1 and abs(n_node - c_node) == 1:
                    port_list = [2, 1]
                rule = GenerateRule(user_info=user_info, node_info=node_info,
                                    next_node_info=NodeTable().pop_node_info(path[node_index+1]),
                                    previous_node_info=NodeTable().pop_node_info(path[node_index-1]),
                                    port=port_list, vlan=vlan, queue_id=queue, priority=priority, server_ip=server_ip).mp()
                self.add_rule(ap=ap, app_type=app_type, user_ip='mp_for_{}_{}'.format(ap, app_type), rule_list=rule, node_name=node_info['node_name'])
        
    def dict_of_queue(self):
        q = {'5': 3, '6': 2, '7': 4, '8': 5,
             '15': 3, '16': 2, '17': 4, '18': 5}
        return q
    
    def assign_priority(self, btype):
        if btype == 'normal':
            return 100
        elif btype == 'super':
            return 300
        else:
            return 200