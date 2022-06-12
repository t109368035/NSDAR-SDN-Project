import pyshark
capture = pyshark.RemoteCapture('192.168.1.15', 'eth0', bpf_filter='dst port 53 and src net 10.10.2.0/24')
capture.sniff(packet_count=1)
capture.close()

i=0
for packet in capture.sniff_continuously(packet_count=1):
    i+=1
    #try: 
    print(packet['IP'].src + ':' + str(i))
    #except:
    #    pass