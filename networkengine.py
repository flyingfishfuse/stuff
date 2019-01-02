# coding=utf-8
"""
LICENSE http://www.apache.org/licenses/LICENSE-2.0
"""

import os
import re
import sys
import time
import time
import scapy
import datetime
import ipaddress
from bs4 import *
try:
    import SocketServer
except ImportError:
    import socketserver
from dnslib import *
from operator import *
import multiprocessing
import pyric.pyw as pyw
from colorama import init
from multiprocessing import Process
from colorama import Fore, Back, Style

init(autoreset=True)
######################################################
#
# VARIABLES AND STUFF
# CHANGE YOUR OPTIONS TO REFLECT YOUR REALITY PLEASE
# IM NOT RESPONSIBLE FOR YOUR LACK OF PERSPECTIVE DUDE
######################################################

classaaddress   = '10.0.0.0'
classbaddress   = '172.16.0.0'
classcaddress   = '192.168.0.0'
clientlist      = {}
mitmlist        = []
wirelessaps     = {}
D               = 'moop.com'
IP              = '192.168.1.1'
TTL             = 60 * 5
PORT            = 6065
sniffiface      = 'eno1'

# httpGET scanner options
HTTPGETarray    = []
getfilename     = 'HTTPGET.sniffed'
httpGETfile     = open(getfilename, 'w')


######################################################
#
#    NETWORK ENGINE
#
######################################################

class Networkz:
    def __init__(self,iface='eth0',mac='de-ad-be',ipclass='c',hostb='24'):
        self.iface                 = iface
        self.moniface              = 'mon0'
        self.mac                   = 'de-ad-be'
        self.ipclass               = ipclass
        self.macaddress            = ''
        self.channel               = '9'
        self.hostbits              = hostb
        self.spoofedhosts          = []
        self.menunumber            = None
        self.httpGETlistenerswitch = False
        self.arpspooferswitch      = False
        self.DNSsniperswitch       = False
        menu()

    def offswitch():
        self.httpGETlistenerswitch = False
        self.arpspooferswitch      = False
        self.DNSsniperswitch       = False

###########################################
#
#           Header printer
#    WIERD indent error here!!!
#############################################

    def httpGETlistener():
        while self.httpGETlistenerswitch == True:
            sniff(iface=sniffiface, prn=GET_print, lfilter=lambda p: "GET" in str(p), filter="tcp port 80")

    def GET_print(packet):
          stars = lambda n: "*" * n
          return "\n".join((stars(40) + "GET PACKET" + stars(40), "\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n")), stars(90)))

    def monifacesend(packet):
        send(packet , iface = self.moniface)

    def makenetworkaddresspool(self, ipclass, hostbits):
        if ipclass == 'c' :
            self.ipclasspool = ipaddress.ip_network(classcaddress + '/' + hostbits)
            self.netmask = ipaddress.ip_address(classcaddress + '/' + hostbits)
            self.ipaddress = str(self.ipclasspool[1])
            self.broadcast = str(ipaddress.ip_address(classcaddress + '/' + hostbits).broadcast)
        elif ipclass == 'b':
            self.ipclasspool = ipaddress.ip_network(classbaddress + '/'  + hostbits)
            self.netmask = ipaddress.ip_address(classbaddress + '/' + hostbits)
            self.ipaddress = str(self.ipclasspool[1])
            self.broadcast = str(ipaddress.ip_address(classbaddress + '/' + hostbits).broadcast)
        elif ipclass == 'a' :
            self.ipclasspool = ipaddress.ip_network(classaaddress + '/' + hostbits)
            self.netmask = str(ipaddress.ip_address(classaaddress + '/' + hostbits).netmask)
            self.ipaddress = str(self.ipclasspool[1])
            self.broadcast = str(ipaddress.ip_address(classaaddress + '/' + hostbits).broadcast)
        else:
            return None

    def iptables():
    # build a rule chain for packet forwarding
    # make sure to remember dns poisoning!
    #make sure to replace static names with variables!
        self.rule.src = "192.168.1.0/255.255.255.0"


        print(os.popen("iptables --flush").read())
        print(os.popen("iptables --table nat --flush").read())
        print(os.popen("iptables --delete-chain").read())
        print(os.popen("iptables --table nat --delete-chain").read())
        print(os.popen("echo 1 > /proc/sys/net/ipv4/ip_forward").read())
        print(os.popen("iptables --table nat --append POSTROUTING --out-interface wlan0 -j MASQUERADE").read())
        print(os.popen("iptables --append FORWARD --in-interface at0 -j ACCEPT").read())
        print(os.popen("iptables -t nat -A PREROUTING -p udp --dport 53 -j DNAT --to 192.168.1.1").read())


    def breakmonitor():
        self.iface = pyw.devadd(m0,'wlan0','managed') # restore wlan0 in managed mode
        pyw.devdel(self.moniface) # delete the monitor interface
        pyw.setmac(self.iface, self.macaddress) # restore the original mac address
        pyw.up(self.iface) # and bring the card up

    def enableipforwarding():
        print("\n[*] Enabling IP Forwarding...\n")
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    def disableipforwarding():
        print("[*] Disabling IP Forwarding...")
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
