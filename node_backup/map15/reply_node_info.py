import paho.mqtt.client as mqtt
import json, time, threading, os, re
import iperf3

MQTT_BROKER = '192.168.1.143'
MQTT_PORT = 1883
MQTT_ALIVE = 60

class MQTT():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_ALIVE)
        self.first_time_send_fail = False
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("Connected with result code "+str(rc))
        self.client.subscribe('info_request')

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode("utf-8").strip('"')
        if data == 'dpidrequest':
            self.dpid_info()
        elif data == 'test1':
            parameters = self.ch_parameter_collect('10.10.1.55')
            parameters['start'] = 'map15'
            parameters['end'] = 'mp55'
            self.publish('node_info', {'chquality': parameters})

    def subscribe(self):
        self.client.on_message = self.on_message
        self.client.loop_forever()
    
    def publish(self, topic, parameters):
        data = json.dumps(parameters)
        self.client.publish(topic, data)
    
    def dpid_info(self):
        dpid = os.popen("sudo ovs-ofctl -O openflow13 show ovsbr |grep -P -o '(?<=dpid:)[a-z0-9]{16}'").read().strip('\n')
        if dpid:
            mac = os.popen("ifconfig ovsbr |grep -P -o '(?<=ether )[a-z0-9]+:[a-z0-9]+:[a-z0-9]+:[a-z0-9]+:[a-z0-9]+:[a-z0-9]+'").read().strip('\n')
            data = {'dpidinfo': {'map15': {'dpid': str(int(dpid, 16)), 'mac': mac}}}
            print('{} ==> reply nodeinfo'.format(time.ctime()))
            self.publish('node_info', data)
        #elif not(dpid):
        #    fail_msg = {'fail': 'map15'}
        #    print('{} ==> reply failmsg'.format(time.ctime()))
        #    print(fail_msg)
        #    self.publish('node_info', fail_msg)
            
    def ch_parameter_collect(self, host):
        bandwidth = self.iperf_measure(host)
        etx = self.etx_extract(host)
        return {'bandwidth': bandwidth, 'etx': etx}
    
    def iperf_measure(self, host):
        iperf_client = iperf3.Client()
        iperf_client.duration = 1 # Measurement time [sec]
        iperf_client.server_hostname = host # Server's IP address
        iperf_client.port = 5202
        result = iperf_client.run()
        if result.error:
            return None
        else:
            return float(result.sent_bps)
    
    def etx_extract(self, host):
        data = os.popen("echo /link | nc localhost 2006 | grep {}".format(host)).read()
        return float(re.search('\d+.\d+(?=\Wt\Wn)', repr(data)).group())

if __name__ == '__main__':
    nodeinfo = MQTT()
    nodeinfo.subscribe()
