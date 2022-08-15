#!/bin/bash

#innitial ovs(map) rule
##table:0
###dhcp
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=61000,table=0,udp,tp_src=67,actions=normal"
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=61000,table=0,udp,tp_src=68,actions=normal"
###arp
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=61000,table=0,arp,in_port=3,actions=LOCAL"
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=61000,table=0,arp,in_port=LOCAL,actions=output:3"
###olsr
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=61000,table=0,udp,in_port=1,nw_src=10.10.1.55,tp_src=698,actions=LOCAL"
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=61000,table=0,udp,in_port=LOCAL,nw_src=10.10.1.15,tp_src=698,actions=output:wlan0"
###iperf test
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=6000,table=0,tcp,tp_src=5202,actions=LOCAL"
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=6000,table=0,tcp,tp_dst=5202,actions=output:wlan0"
###transfer client packet
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=100,table=0,in_port=3,ip,nw_src=10.10.2.0/24,actions=goto_table:1"
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=100,table=0,in_port=1,ip,nw_dst=10.10.2.0/24,actions=goto_table:2"
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=100,table=0,in_port=2,ip,nw_dst=10.10.2.0/24,actions=goto_table:2"

##table:2
###pop vlan
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=100,table=2,vlan_tci=0x1000/0x1000,actions=pop_vlan,goto_table:4"

exit 0