#!/bin/bash

#start allow remote capture
sudo rpcapd -n &

#start allow extract node infomation
python3 /home/pi/Desktop/reply_node_info.py &

#innitial ovs rule
## table:0
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=61000,table=0,udp,in_port=1,nw_src=10.10.1.56,tp_src=698,actions=LOCAL"
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=61000,table=0,udp,in_port=1,nw_src=10.10.1.46,tp_src=698,actions=LOCAL"
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=61000,table=0,udp,in_port=LOCAL,nw_src=10.10.1.16,tp_src=698,actions=output:wlan0"
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=6000,table=0,tcp,tp_src=5202,actions=LOCAL"
sudo ovs-ofctl add-flow -O OpenFlow13 ovsbr "priority=6000,table=0,tcp,tp_dst=5202,actions=output:wlan0"

#add arp table
sudo arp -s 10.10.1.56 dc:a6:32:1b:0b:c1 -i ovsbr
sudo arp -s 10.10.1.46 dc:a6:32:85:0e:74 -i ovsbr
sudo arp -s 10.10.1.99 dc:a6:32:85:0e:aa -i ovsbr

#start olsr
sudo olsrd

exit 0
