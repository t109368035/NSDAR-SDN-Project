#!/bin/bash

#start allow remote capture
sudo rpcapd -n &

#start allow extract node infomation
python3 /home/pi/Desktop/reply_node_info.py &

#innitial ovs rule
##table:0
#sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,arp,action=normal"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=1,nw_src=10.10.1.6,tp_src=698,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=1,nw_src=10.10.1.89,tp_src=698,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=1,nw_src=10.10.1.16,tp_src=698,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=1,nw_src=10.10.1.99,tp_src=698,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=61000,table=0,udp,in_port=LOCAL,nw_src=10.10.1.46,tp_src=698,action=output:wlan0"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=6000,table=0,tcp,tp_src=5202,action=output:wlan0"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=6000,table=0,tcp,tp_dst=5202,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=6000,table=0,tcp,tp_src=5201,action=LOCAL"
sudo ovs-ofctl add-flow -O openflow13 ovsbr "priority=6000,table=0,tcp,tp_dst=5201,action=output:wlan0"

#add arp table
sudo arp -s 10.10.1.6 dc:a6:32:85:0f:07 -i ovsbr
sudo arp -s 10.10.1.89 dc:a6:32:85:0f:bb -i ovsbr
sudo arp -s 10.10.1.16 dc:a6:32:85:04:f6 -i ovsbr
sudo arp -s 10.10.1.99 dc:a6:32:85:0e:aa -i ovsbr

#start olsr
sudo olsrd

exit 0
