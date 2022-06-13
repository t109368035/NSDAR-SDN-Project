import pyshark

capture = pyshark.RemoteCapture('192.168.1.', 'eth0', bpf_filter='ip src host 10.10.2')
