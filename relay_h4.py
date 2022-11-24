#!/usr/bin/env python3
#h4 recieve packet and forward it to s3-eth1
from scapy.all import *

def send_to_s3(packets):
    print(f"{len(packets)} packets to s")
    sendp(packets,iface='h4-eth0')

#h1-eth1 to h4-eth1 
conf.iface="h4-eth1"
#sniff broadcast 
print("running")
#sniff lldp brodcast
sniff(prn=send_to_s3)
