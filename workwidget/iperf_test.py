import paho.mqtt.client as mqtt
import json, time

MQTT_BROKER = '192.168.1.143'
MQTT_PORT = 1883
MQTT_ALIVE = 60
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, MQTT_ALIVE)

def publish(topic, parameters):
    data = json.dumps(parameters)
    client.publish(topic, data)

def iperf_test_request():
    try:
        publish('info_request', 'test1')
        time.sleep(1)
        publish('info_request', 'test2')
        time.sleep(1)
        publish('info_request', 'test3')
        time.sleep(1)
        publish('info_request', 'test4')
        return 'iperf request already send'
    except:
        return 'iperf request ERROR'

iperf_test_request()
time.sleep(5)