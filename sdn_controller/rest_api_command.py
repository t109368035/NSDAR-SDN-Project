import requests

def get_all_switches():
    url = "http://localhost:8080/stats/switches"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    dpid_list = response.text.replace('[','')
    dpid_list = dpid_list.replace(']','')
    dpid_list = dpid_list.replace(' ','')
    dpid_list = dpid_list.split(',')

    return dpid_list

def add_a_flow_entry(payload):
    url = "http://localhost:8080/stats/flowentry/add"

    headers = {
    'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return str(response)

