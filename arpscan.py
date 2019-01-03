 #!/usr/bin/python
# coding=utf-8
"""
LICENSE http://www.apache.org/licenses/LICENSE-2.0
"""

import os
import sys
from scapy.all import *
import argparse

parser = argparse.ArgumentParser(description='some network tools')
parser.add_argument('--arpscanner',
                                   dest    ='scanner',
                                   action  ="store_true" ,
                                   default = False ,
                                   help    = "switches the scanner on, scans for live hosts using arp" )

parser.add_argument('--arpspoof',
                                 dest    = 'spoofer',
                                 action  = "store_true" ,
                                 default = False ,
                                 help    = "switches the spoofer on, does smart, responsive spoofing instead of flooding")

parser.add_argument('--macchange',
                                 dest    = 'macchange',
                                 action  = "store_true" ,
                                 default = False ,
                                 help    = "switches your mac address and selects your card")




networkcard     = ''
myip            = '192.168.0.3'
mymacaddress    = "b4:b5:2f:cf:75:42"
iface1          = 'eno1'
hostlist        = []
def arpscanner():
    while True:
        try:
            sniff(lfilter = lambda x: x.haslayer(ARP), prn = arpscan, store = False )
        except KeyboardInterrupt:
            break
def arpscan(pkt):
    try:
        if pkt[ARP].op == 1:
            hostlist.append((pkt.psrc , pkt.hwsrc))
        setclean = set(hostlist)
        cleanhostlist = list(setclean)
        for each in cleanhostlist:
            print("Live host at: " + each[0])
    except KeyboardInterrupt:
        sys.exit(0)

def arpsniffer():
    while True:
        try:
            sniff(lfilter = lambda x: x.haslayer(ARP), prn = arpspoofer, store = False )
        except KeyboardInterrupt:
            break

def arpprinter():
    while True:
        try:
            sniff(lfilter = lambda x: x.haslayer(ARP), prn = lambda x: x.summary() , store = False)
        except KeyboardInterrupt:
            break

def signal_handler(signal, frame):
      p.terminate()
      p.join()

argument = parser.parse_args()
if argument.scanner == True :
    arpscanner()
elif argument.spoofer == True :
    arpsniffer()
