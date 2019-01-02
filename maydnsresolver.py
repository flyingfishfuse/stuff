import requests
from bs4 import BeautifulSoup
import lxml
import os
import re
import argparse
import io
import time
import multiprocessing
import nmap

parser = argparse.ArgumentParser(description='DNS host enumerating machine with subsequent port scanning... youre gonna fry your processor if you arent careful.')

parser.add_argument('--scanner',     dest='scanner',    action="store_true" , default = False , help = "switches the scanner on, with no arguments it simply port scans each host allowing you to choose to skip on a timer" )
parser.add_argument('--robots',      dest='robots',     action="store_true" , default = False , help = "Categories: default, safe. Checks for disallowed entries in robots.txt.")
parser.add_argument('--rpcscan',     dest='rpc',        action="store_true" , default = False , help = "Categories: default, safe, discovery. Connects to portmapper and fetches a list of all registered programs. ")
parser.add_argument('--httptrace',   dest='httptrace',  action="store_true" , default = False , help = "Categories: discovery. Sends an HTTP TRACE request and shows header fields that were modified in the response.")
parser.add_argument('--httpauth',    dest='httpauth',   action="store_true" , default = False , help = "Categories: default, auth, intrusive. Gets the authentication scheme and realm of a web service that requires authentication.")
parser.add_argument('--httppasswd',  dest='httppasswd', action="store_true" , default = False , help = "Categories: intrusive, vuln. Checks if a web server is vulnerable to directory traversal by attempting to retrieve /etc/passwd.")
parser.add_argument('--netbiosstat', dest='netbiosstat',action="store_true" , default = False , help = "Categories: default, discovery, safe. Attempt\'s to get the target\'s NetBIOS names and MAC address. By default, the script displays the name of the computer and the logged-in user; if the verbosity is turned up, it displays all names the system thinks it owns. For more information on the NetBIOS protocol, see nmap/nselib/netbios.lua")
#parser.add_argument('--domain', dest = 'domain', type = str , store = 'true' , default = 'www.Google.com')
#begin the great equalsing!
httpport             = [80 , 443]
netbiosports         = [137 , 139 , 139]
rpc                  = 'rpcinfo.nse '# (rpcinfo)
robots               = 'robots.nse'  #(robots.txt)
httpauth             = 'HTTPAuth.nse' #(HTTP Auth)Categories: default, auth, intrusive. Gets the authentication scheme and realm of a web service that requires authentication.
netbiosstat          = 'nbstat.nse' #(NBSTAT)
httptrace            = 'HTTPtrace.nse' #(HTTP TRACE)Categories: discovery. Sends an HTTP TRACE request and shows header fields that were modified in the response.
httppasswd           = 'HTTPpasswd.nse' #(HTTP directory traversal passwd probe)Categories: intrusive, vuln. Checks if a web server is vulnerable to directory traversal by attempting to retrieve /etc/passwd.
argument             = parser.parse_args()
script_name          = ''
path_to_nmap_scripts = 'usr/share/nmap/scripts/'
nmapscriptarguments  ='--script=' + path_to_nmap_scripts + script_name
nmapscriptlist       = open('nmapscriptlist.txt')
# instantiate nmap.PortScanner object
argument             = parser.parse_args()
dlist                = []
dlist1               = []
dlist2               = []
scantask             = []
tasklist2            = []

#domainregex = re.match( re'^[a-z0-9]([a-z0-9-]+\.){1,}[a-z0-9]+\Z', domain_soup, re.M|re.I)
#print('/n please input the IP address or FQDN of the host you wish to enumerate domains for')
host = '205.186.183.177'
dnsresolver     = "https://viewdns.info/reverseip/"
#dnsresolversite2
#host                 = input('host: ==> ')
head                 = {'Accept' : 'text/html' , 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0' , 'Accept-Charset' : 'utf-8'}
payload              = { 'host' : host , 't': '1', 'submit': 'GO'}
resultsfilesuffix    = '.scan'

def makehostsoup():
    #print('input the host or domain you wish to gather the zone information for')
    #host = input('/n host>')
    file = open(name + time + resultsfilesuffix , "w")
    hostlistrawhtml = requests.get(dnsresolver, params = payload , headers = head)
    soupyhostlistrawhtml = BeautifulSoup(hostlistrawhtml.text , "lxml")
    dirtyrows = soupyhostlistrawhtml.findAll('tr')
    for each in dirtyrows[4]:
        dirtydiv = each.findAll('td')
        dlist.append(dirtydiv)
    for each in dlist:
        for each1 in each:
            domain = regex.search(each1.getText())
            if domain == None :
                None
            else:
                dlist2.append(domain.group())
                for each in dlist2 :
                    file.write(each + '\n')
    file.close()
    return dlist2

def scanner(dname, port, args):
    if port == None:
        scan = nmap.PortScanner()
        results = scan.scan(hosts = dname , arguments = nmapscriptarguments)
    else :
        for each in port:
            results = scan.scan(hosts = dname, port = each, arguments = nmapscriptargumemts)
            print(scan.command_line())

def rpcscanner():
    script_name = rpc
    port = None
    for each in dlist2:
        rpcscan = multiprocessing.Process(scanner(each, port, script_name))

def httpauthscan():
    script_name = httpauth
    port = httpport
    for each in dlist2:
        print('/n HTTP authority parameters :' + each )
        authscan = scanner(each, port, script_name)


def httppasswdscan(domain):
    script_name = httppasswd
    port = httpport
    for each in dlist2:
        print('/n scanning for directory traversal :' + each )
        httppasswdscan = scanner(each, port, script_name)

def netbiosscanscanscan(): # who think of these names!?!?
    script_name = netbiosscan
    port = netbiosport
    for each in dlist2:
        print('/n scanning netbios  :' + each)
        netbiosscanscan = scanner(each, port, script_name)

def httptracescanscan():
    script_name = httptrace
    port = httpport
    for each in dlist2:
        print('HTTP trace scan in progress :' + each)
        httptracescan = scanner(each, port, script_name)

def robotscanner(domain):
    script_name = robots
    port = httpport
    for each in dlist2:
        print('scanning robots.txt on :' + each )
        robotscan = scanner(each , port, script_name)

def savescan(name, content):
    file = open(name + time + resultfilesuffix , "w")
    file.append(content)
    file.close()

#main code loop to start the modules
#run the functions/modules specified in the arguments

def runscanner():
    makehostsoup()
    for each in dlist2:
        print(each)
    if argument.robots == True :
        scantask.append(multiprocessing.Process(target=robotscanner())
    if argument.rpc == True :
        scantask.append(multiprocessing.Process(target=rpcscanner())
    if argument.httptrace == True:
        scantask.append(multiprocessing.Process(target=httptracescanscan())
    if argument.httpauth == True:
        scantask.append(multiprocessing.Process(target=httpauthscan())
    if argument.httppasswd  == True:
        scantask.append(multiprocessing.Process(target=httppasswdscan())
    if argument.netbiosstat == True :
        scantask.append(multiprocessing.Process(target=netbiosscanscanscan())
    for each in jobs:
        each.start()






#print('here is some more information from a different method')
#qname = dns.reversename.from_address('172.217.3.46')
#answer = dns.resolver.query(qname, 'PTR')
#for rr in answer:
# print(rr)
