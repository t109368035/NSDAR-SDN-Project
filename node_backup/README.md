### 網路拓撲架構  
<img src="/image/mesh_topology_detail.png" width="500">

### 節點Python環境
- Python version : 3.6.13
- Python Package :
  - paho-mqtt : 1.5.0
  - iperf3 : 0.1.11

### 設定Wi-Fi國碼為台灣
```
sudo -i
echo "options cfg80211 ieee80211_regdom=TW"  >  /etc/modprobe.d/cfg80211.conf 
```

### 安裝OLSR資訊
```
sudo apt-get install olsrd
```

### 安裝OVS資訊
- [Install OVS tutorial](https://hackmd.io/@TWvQM7zrTEyzbIKJIj8l2w/ryI3JV9wY)

### 安裝rpcapd資訊
- [rpcapd-for-RPi](https://github.com/idkpmiller/rpcapd-for-RPi)

### 安裝DHCP Server資訊(only necessary on map15 and map5)
```
sudo apt-get install isc-dhcp-server
```

### 安裝ntopng資訊(only necessary on map15 and map5)
- [ntopng](https://packages.ntop.org/)

### QoS設定
```
#on local(ovs) add qos rule:
sudo ovs-vsctl -- \
set Port "PortName" qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
    other-config:max-rate=1000000000 \
    queues:0=@q0 \
    queues:1=@q1 \
    queues:2=@q2 \
    queues:3=@q3 \
    queues:4=@q4 \
    queues:5=@q5 -- \
--id=@q0 create queue other-config:max-rate=100000000 -- \
--id=@q1 create queue other-config:max-rate=5000000 -- \
--id=@q2 create queue other-config:max-rate=4000000 -- \
--id=@q3 create queue other-config:max-rate=6000000 -- \
--id=@q4 create queue other-config:max-rate=10000000 -- \
--id=@q5 create queue other-config:max-rate=20000000

#on local(ovs) delete qos rule:
#check qos list
ovs-vsctl list qos
ovs-vsctl -- get Port "PortName" qos

#disconnect qos rule from port(要先解除連結才可以執行刪除的動作)
ovs-vsctl -- clear Port "PortName" qos

#delete qos rule and queue by assign uuid
ovs-vsctl -- destroy Qos "QoS_uuid"
ovs-vsctl -- destroy queue "Queue_uuid"

#delete all of them(Qos and Queue) in one time
ovs-vsctl -- --all destroy Qos -- --all destroy Queue
```
