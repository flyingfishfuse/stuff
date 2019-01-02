 #!/usr/bin/python
# coding=utf-8
"""
LICENSE http://www.apache.org/licenses/LICENSE-2.0
"""

import os
import re
import sys
import time
import json
from scapy.all import *
import socket
import select
import urllib3
import datetime
import threading
import traceback
import ipaddress
import argparse
from bs4 import *
from pyric import *
import multiprocessing as mp
from colorama import init
from multiprocessing import Process
from colorama import Fore, Back, Style
import pyric.pyw as pyw


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


    ######################################################
    #
    #    ARP SPOOFER
    #
    ######################################################

def arpscanner():
    while True: 
        try:
            sniff(lfilter = lambda x: x.haslayer(ARP), prn = arpscan, store = False )
        except KeyboardInterrupt:
            break


    ######################################################
    #
    #    ARP SCANNER
    #
    ######################################################


def arpscan(pkt):
    try:
        if pkt[ARP].op == 1:  
            print(pkt.summary())  
            hostlist.append((pkt.psrc , pkt.hwsrc))
        setclean = set(hostlist)
        cleanhostlist = list(setclean)
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


    ######################################################
    #
    #    Menu System
    #
    ######################################################
def signal_handler(signal, frame):
      p.terminate()
      p.join()

argument = parser.parse_args()
if argument.scanner == True :
    arpscanner()
elif argument.spoofer == True :
    arpsniffer()
elif argument.macchange == True:
    selectiface()

    
