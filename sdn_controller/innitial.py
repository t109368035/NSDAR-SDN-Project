import sdn_controller.rest_api_command as restful_command
from sdn_controller import information
'''
class open_wirless_channel():
    def __init__(self):
        self.dpid_to_bridge = information.all_dpid_to_bridge()
'''

dpid_to_bridge = information.all_dpid_to_bridge()

'''
將port:LOCAL(bridge)收到的封包從port:1(wireless adapter)送出去
將port:1(wireless adapter)收到的封包從port:LOCAL(bridge)送出去
'''    
def innitial_rule():
    conneted_dpid_list = list()
    while len(conneted_dpid_list) != 4: #=> 確認所有ovs都連上controller
        conneted_dpid_list = restful_command.get_all_switches()
    for dpid in conneted_dpid_list:
        payload_local_to_wireless = "{{\"dpid\": {},\"table_id\": 0,\"priority\": 100,\"match\":{{\"in_port\": \"LOCAL\"}},\r\n\"actions\":[{{\"type\":\"OUTPUT\",\"port\": 1}}]}}".format(dpid)
        payload_wireless_to_local = "{{\"dpid\": {},\"table_id\": 0,\"priority\": 100,\"match\":{{\"in_port\": 1}},\r\n\"actions\":[{{\"type\":\"OUTPUT\",\"port\": \"LOCAL\"}}]}}".format(dpid)
        status_local_to_wireless = restful_command.add_a_flow_entry(payload_local_to_wireless)
        status_wireless_to_local = restful_command.add_a_flow_entry(payload_wireless_to_local)
        print(dpid_to_bridge[dpid])
        print("{}: status_local_to_wireless => {}".format(dpid, status_local_to_wireless))
        print("{}: status_wireless_to_local => {}\n".format(dpid, status_wireless_to_local))

"""
if __name__ == '__main__':
    command = open_wirless_channel()
    command.send_API()
"""