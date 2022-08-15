#!/bin/bash

#start allow extract node infomation
python3 /home/pi/Desktop/reply_node_info.py &

#innitial ovs rule
bash /home/pi/Desktop/ovs_rule_map.sh

## add arp table
sudo arp -s 10.10.1.55 dc:a6:32:1b:29:e2 -i ovsbr
sudo arp -s 10.10.1.98 dc:a6:32:85:0f:d9 -i ovsbr

#start olsr
sudo olsrd

#start allow remote capture
sudo rpcapd -n -b 192.168.1.15 -d -4 -l 192.168.1.143

exit 0
