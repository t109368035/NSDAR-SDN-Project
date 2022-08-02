import requests, time

class GenerateRule:
    def __init__(self, user_info, node_info, next_node_info, previous_node_info, port, vlan, queue_id, priority, cookie=0, server_ip=None):
        self.user_info = user_info
        self.node_info = node_info
        self.next_node_info = next_node_info
        self.previous_node_info = previous_node_info
        self.port = port
        self.queue_id = queue_id
        self.vlan_vid = int(vlan) + 4096
        self.cookie = cookie
        self.priority = priority
        self.server_ip = dict()
        if server_ip:
            self.server_ip['dst'] = ',"ipv4_dst":"{}"'.format(server_ip)
            self.server_ip['src'] = ',"ipv4_src":"{}"'.format(server_ip)
        else:
            self.server_ip['dst'] = ''
            self.server_ip['src'] = ''
        
    def map(self):
        table1_push_vlan = '{{"dpid":{},"cookie":{},"table_id":1,"priority":{},"match":{{"ipv4_src":"{}"{},"eth_type":2048}},"actions":[{{"type":"PUSH_VLAN","ethertype":33024}},{{"type":"SET_FIELD","field":"vlan_vid","value":{}}},{{"type":"GOTO_TABLE","table_id":3}}]}}'.format(self.node_info['node_dpid'], self.cookie, self.priority, self.user_info['user_ip'], self.server_ip['dst'], self.vlan_vid)
        table4_to_device = '{{"dpid":{},"cookie":{},"table_id":4,"priority":{},"match":{{"ipv4_dst":"{}","eth_type":2048,"eth_dst":"{}","eth_src":"{}"}},"actions":[{{"type":"SET_FIELD","field":"eth_src","value":"{}"}},{{"type":"SET_FIELD","field":"eth_dst","value":"{}"}},{{"type":"OUTPUT","port":3}}]}}'.format(self.node_info['node_dpid'], self.cookie, self.priority, self.user_info['user_ip'], self.node_info['node_mac'], self.next_node_info['node_mac'], self.node_info['node_mac'], self.user_info['user_mac'])
        return [table1_push_vlan, table4_to_device]
    
    def map_to_node(self):
        table3_to_node = '{{"dpid":{},"cookie":{},"table_id":3,"priority":{},"match":{{"dl_vlan": {}}},"actions":[{{"type":"SET_FIELD","field":"eth_src","value":"{}"}},{{"type":"SET_FIELD","field":"eth_dst","value":"{}"}},{{"type":"SET_QUEUE","queue_id":{}}},{{"type":"OUTPUT","port":{}}}]}}'.format(self.node_info['node_dpid'], self.cookie, self.priority, self.vlan_vid, self.node_info['node_mac'],  self.next_node_info['node_mac'], self.queue_id, self.port)
        return [table3_to_node]

    def mp(self): ##output port 選擇
        table0_to_next_node = '{{"dpid":{},"cookie":{},"table_id":0,"priority":{},"match":{{"dl_vlan":{},"eth_src": "{}","eth_dst": "{}"}},"actions":[{{"type":"SET_FIELD","field":"eth_src","value":"{}"}},{{"type":"SET_FIELD","field":"eth_dst","value":"{}"}},{{"type":"OUTPUT","port":{}}}]}}'.format(self.node_info['node_dpid'], self.cookie, self.priority, self.vlan_vid, self.previous_node_info['node_mac'], self.node_info['node_mac'], self.node_info['node_mac'], self.next_node_info['node_mac'], self.port[0])
        table0_to_previous_node = '{{"dpid":{},"cookie":{},"table_id":0,"priority":{},"match":{{"dl_vlan":{},"eth_src": "{}","eth_dst": "{}"}},"actions":[{{"type":"SET_FIELD","field":"eth_src","value":"{}"}},{{"type":"SET_FIELD","field":"eth_dst","value":"{}"}},{{"type":"OUTPUT","port":{}}}]}}'.format(self.node_info['node_dpid'], self.cookie, self.priority, self.vlan_vid, self.next_node_info['node_mac'], self.node_info['node_mac'], self.node_info['node_mac'], self.previous_node_info['node_mac'], self.port[1])
        return [table0_to_next_node, table0_to_previous_node]
    
    def mpp(self):
        table1_push_vlan = '{{"dpid":{},"cookie":{},"table_id":1,"priority":{},"match":{{"ipv4_dst":"{}"{},"eth_type":2048}},"actions":[{{"type":"PUSH_VLAN","ethertype":33024}},{{"type":"SET_FIELD","field":"vlan_vid","value":{}}},{{"type":"GOTO_TABLE","table_id":3}}]}}'.format(self.node_info['node_dpid'], self.cookie, self.priority, self.user_info['user_ip'], self.server_ip['src'], self.vlan_vid)
        table4_to_internet = '{{"dpid":{},"cookie":{},"table_id":4,"priority":{},"match":{{"ipv4_src":"{}","eth_type":2048,"eth_dst":"{}","eth_src":"{}"}},"actions":[{{"type":"SET_FIELD","field":"eth_src","value":"{}"}},{{"type":"OUTPUT","port":"LOCAL"}}]}}'.format(self.node_info['node_dpid'], self.cookie, self.priority, self.user_info['user_ip'], self.node_info['node_mac'], self.previous_node_info['node_mac'], self.user_info['user_mac'])
        return [table1_push_vlan, table4_to_internet]
    
    def mpp_to_node(self):
        table3_to_node = '{{"dpid":{},"cookie":{},"table_id":3,"priority":{},"match":{{"dl_vlan": {}}},"actions":[{{"type":"SET_FIELD","field":"eth_dst","value":"{}"}},{{"type":"SET_QUEUE","queue_id":{}}},{{"type":"OUTPUT","port":1}}]}}'.format(self.node_info['node_dpid'], self.cookie, self.priority, self.vlan_vid, self.previous_node_info['node_mac'], self.queue_id)
        return [table3_to_node]

class RetrieveSwitchStats:
    def __init__(self, dpid):
        self.dpid = dpid

    def get_Mission_flow_bitrate(self, node, p_byte):
        url = "http://127.0.0.1:8080/stats/flow/"+self.dpid
        match = '{{"table_id":3,"cookie":{},"cookie_mask":{}}}'.format(node+3, node+3)
        flow_info = eval(self.post_request(url, match))[self.dpid]
        #print(flow_info)
        if not flow_info:
            return 0, 0
        else:
            n_byte = flow_info[0]['byte_count']
            bitrate = (((n_byte - p_byte)*8)/20)/1000000
            return bitrate, n_byte

    def post_request(self, url, match):
        headers = {'Content-Type': 'text/plain'}
        response = requests.request("POST", url, headers=headers, data=match)
        send_restapi = str(response)
        getinfo = response.text
        response.close()
        if '200' not in str(send_restapi):
            print('get in post request retry(RetrieveSwitchStats)')
            time.sleep(0.3)
            self.post_request(self.rule, self.action)
        else:
            return getinfo
        