#!/bin/bash

#let ovsbr connect internet
sudo iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
#let ovsbr connect lan
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo ip route add 10.10.2.0/24 via 10.10.1.88 dev ovsbr


#start allow remote capture
sudo rpcapd -n &

#start allow extract node infomation
python3 /home/pi/Desktop/reply_node_info.py &

# innitial ovs rule
##table:0
#sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,arp,action=normal"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=1,nw_src=10.10.1.45,tp_src=698,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=LOCAL,nw_src=10.10.1.88,tp_src=698,action=output:wlan0"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=6000,table=0,tcp,tp_src=5201,action=output:wlan0"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=6000,table=0,tcp,tp_dst=5201,action=LOCAL"
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=100,table=0,in_port=1,actions=goto_table:2"
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=100,table=0,in_port=LOCAL,actions=goto_table:1"

##table:2
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=100,table=2,vlan_tci=0x1000/0x1000,actions=pop_vlan,goto_table:4"

#add arp table
sudo arp -s 10.10.1.45 dc:a6:32:85:0f:f4 -i ovsbr

#start olsr
sudo olsrd

exit 0
