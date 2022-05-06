class PostRestAPI:
    def __init__(self, user_info, node_info, next_node_info, previous_node_info, port, queue_id=3):
        self.user_info = user_info
        self.node_info = node_info
        self.next_node_info = next_node_info
        self.previous_node_info = previous_node_info
        self.port = port
        self.queue_id = queue_id
        self.vlan_vid = int(self.user_info['user_vlan']) + 4096

    def map(self):
        table1_push_vlan = '{{"dpid":{},"table_id":1,"priority":100,"match":{{"ipv4_src":"{}","eth_type":2048}},"actions":[{{"type":"PUSH_VLAN","ethertype":33024}},{{"type":"SET_FIELD","field":"vlan_vid","value":{}}},{{"type":"GOTO_TABLE","table_id":3}}]}}'.format(self.node_info['node_dpid'], self.user_info['user_ip'], self.vlan_vid)
        table3_to_node = '{{"dpid":{},"table_id":3,"priority":100,"match":{{"dl_vlan": {}}},"actions":[{{"type":"SET_FIELD","field":"eth_src","value":"{}"}},{{"type":"SET_FIELD","field":"eth_dst","value":"{}"}},{{"type":"SET_QUEUE","queue_id":{}}},{{"type":"OUTPUT","port":{}}}]}}'.format(self.node_info['node_dpid'], self.vlan_vid, self.node_info['node_mac'],  self.next_node_info['node_mac'], self.queue_id, self.port)
        table4_to_device = '{{"dpid":{},"table_id":4,"priority":100,"match":{{"ipv4_dst":"{}","eth_type":2048,"eth_dst":"{}","eth_src":"{}"}},"actions":[{{"type":"SET_FIELD","field":"eth_src","value":"{}"}},{{"type":"SET_FIELD","field":"eth_dst","value":"{}"}},{{"type":"OUTPUT","port":3}}]}}'.format(self.node_info['node_dpid'], self.user_info['user_ip'], self.node_info['node_mac'], self.next_node_info['node_mac'], self.node_info['node_mac'], self.user_info['user_mac'])
        return [table1_push_vlan, table3_to_node, table4_to_device]

    def mp(self): ##output port 選擇
        table0_to_next_node = '{{"dpid":{},"table_id":0,"priority":100,"match":{{"dl_vlan":{},"eth_src": "{}","eth_dst": "{}"}},"actions":[{{"type":"SET_FIELD","field":"eth_src","value":"{}"}},{{"type":"SET_FIELD","field":"eth_dst","value":"{}"}},{{"type":"OUTPUT","port":{}}}]}}'.format(self.node_info['node_dpid'], self.vlan_vid, self.previous_node_info['node_mac'], self.node_info['node_mac'], self.node_info['node_mac'], self.next_node_info['node_mac'], self.port[0])
        table0_to_previous_node = '{{"dpid":{},"table_id":0,"priority":100,"match":{{"dl_vlan":{},"eth_src": "{}","eth_dst": "{}"}},"actions":[{{"type":"SET_FIELD","field":"eth_src","value":"{}"}},{{"type":"SET_FIELD","field":"eth_dst","value":"{}"}},{{"type":"OUTPUT","port":{}}}]}}'.format(self.node_info['node_dpid'], self.vlan_vid, self.next_node_info['node_mac'], self.node_info['node_mac'], self.node_info['node_mac'], self.previous_node_info['node_mac'], self.port[1])
        return [table0_to_next_node, table0_to_previous_node]
    
    def mpp(self):
        table1_push_vlan = '{{"dpid":{},"table_id":1,"priority":100,"match":{{"ipv4_dst":"{}","eth_type":2048}},"actions":[{{"type":"PUSH_VLAN","ethertype":33024}},{{"type":"SET_FIELD","field":"vlan_vid","value":{}}},{{"type":"GOTO_TABLE","table_id":3}}]}}'.format(self.node_info['node_dpid'], self.user_info['user_ip'], self.vlan_vid)
        table3_to_node = '{{"dpid":{},"table_id":3,"priority":100,"match":{{"dl_vlan": {}}},"actions":[{{"type":"SET_FIELD","field":"eth_dst","value":"{}"}},{{"type":"SET_QUEUE","queue_id":{}}},{{"type":"OUTPUT","port":1}}]}}'.format(self.node_info['node_dpid'], self.vlan_vid, self.previous_node_info['node_mac'], self.queue_id)
        table4_to_internet = '{{"dpid":{},"table_id":4,"priority":100,"match":{{"ipv4_src":"{}","eth_type":2048,"eth_dst":"{}","eth_src":"{}"}},"actions":[{{"type":"SET_FIELD","field":"eth_src","value":"{}"}},{{"type":"OUTPUT","port":"LOCAL"}}]}}'.format(self.node_info['node_dpid'], self.user_info['user_ip'], self.node_info['node_mac'], self.previous_node_info['node_mac'], self.user_info['user_mac'])
        return [table1_push_vlan, table3_to_node, table4_to_internet]