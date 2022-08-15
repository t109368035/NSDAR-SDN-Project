#!/bin/bash

#let ovsbr connect internet
sudo iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
#let ovsbr connect lan
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
#let client packet route to outside
sudo ip route add 10.10.2.0/24 via 10.10.1.99 dev ovsbr

#start allow remote capture
sudo rpcapd -n &

#start allow extract node infomation
python3 /home/pi/Desktop/reply_node_info.py &

# innitial ovs rule
##table:0
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=1,nw_src=10.10.1.56,tp_src=698,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=1,nw_src=10.10.1.46,tp_src=698,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=LOCAL,nw_src=10.10.1.99,tp_src=698,action=output:wlan0"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=6000,table=0,tcp,tp_src=5201,action=output:wlan0"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=6000,table=0,tcp,tp_dst=5201,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=100,table=0,in_port=1,actions=goto_table:2"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=100,table=0,in_port=LOCAL,actions=goto_table:1"
##table:2
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=100,table=2,vlan_tci=0x1000/0x1000,actions=pop_vlan,goto_table:4"

#add arp table
sudo arp -s 10.10.1.56 da:a6:32:1b:0b:c1 -i ovsbr
sudo arp -s 10.10.1.46 dc:a6:32:85:0e:74 -i ovsbr
sudo arp -s 10.10.1.16 da:a6:32:85:04:f6 -i ovsbr

#start olsr
sudo olsrd

exit 0
