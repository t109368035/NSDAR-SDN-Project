#!/bin/bash

#start allow remote capture
sudo rpcapd -n &

#start allow extract node infomation
python3 /home/pi/Desktop/reply_node_info.py &

#innitial ovs rule
##table:0
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=1,nw_src=10.10.1.15,tp_src=698,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=1,nw_src=10.10.1.98,tp_src=698,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=LOCAL,nw_src=10.10.1.55,tp_src=698,action=output:wlan0"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=6000,table=0,tcp,tp_src=5202,action=output:wlan0"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=6000,table=0,tcp,tp_dst=5202,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=6000,table=0,tcp,tp_src=5201,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=6000,table=0,tcp,tp_dst=5201,action=output:wlan0"

#add arp table
sudo arp -s 10.10.1.15 dc:a6:32:84:e1:74 -i ovsbr
sudo arp -s 10.10.1.98 dc:a6:32:85:0f:d9 -i ovsbr

#start olsr
sudo olsrd

exit 0
