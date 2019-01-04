#!/bin/python
import requests
import os
import argparse
from bs4 import BeautifulSoup
import time
#OPTIONS!
parser = argparse.ArgumentParser(description='Brute-Force fuzzer for all methods and options, regexes for a reflection in the response')
parser.add_argument('--file',
                                 dest    = 'file',
                                 action  = "store" ,
                                 default = 'simplebackdoor.php' ,
                                 help    = "The file you are wanting to upload or payload you wish to test" )
parser.add_argument('--cookie',
                                 dest    = 'cookie',
                                 action  = "store" ,
                                 default = 'cookie.txt' ,
                                 help    = "this file is a cookie jar! Only big enough for one cookie! Put a cookie recipie you wish to send along with ... y'know... whatever" )

parser.add_argument('--target',
                                 dest    = 'target',
                                 action  = "store" ,
                                 default = 'http://127.0.0.1' ,
                                 help    = "TARGET to attack, defaults to localhost. Don't forget the http://" )

parser.add_argument('--xforwardedfor',
                                 dest    = 'xforward',
                                 action  = "store" ,
                                 default = '127.0.0.1' ,
                                 help    = "Sets the X-Forwarded-For header to... something" )
parser.add_argument('--xforwardedip',
                                 dest    = 'xforwardip',
                                 action  = "store" ,
                                 default = '127.0.0.1' ,
                                 help    = "Sets the X-Forward-IP header to... something" )


arguments = parser.parse_args()

class  Uploader:
    """required arguments are the url, method, and filename."""
    def __init__(self):
        self.header         = {}
        self.uploadfilename = uploadfilename
        self.fileobj        = openfile(self.uploadfilename)
        self.savefile       = 'headers : '
        self.url            = arguments.target
        self.xforward       = arguments.xforward
        self.xforwardip     = arguments.xforwardedip
        self.useragent      = 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0'
        self.mimetype       = ''

        self.mimelist       = mimelist = ['text/plain',
                                        'application/octet-stream',
                                        'text/css',
                                        'text/html',
                                        'text/javascript',
                                        'image/gif',
                                        'image/jpeg',
                                        'image/png',
                                        'image/svg-xml']
        self.methodlist     = ['get', 'post','put','head','delete', 'patch','options']
        self.methodholder   = ''

        if self.xforward != None:
            self.header.update({'X-Forwarded-For' : self.xforward})
        if self.xforwardip != None:
            self.header.update({'X-Forwarded-IP' : self.xforward})
        if arguments.cookiejar != None:
            self.cookie = openfile(self.cookiejar) #pulling a cookie from the jar!
        #this starts the gunplay
        fuzzer(self.url, self.fileobj)

    def openfile(filename):
        try:
            fileobject = open(arguments.file, 'rb')
            return fileobject
        except OSError as error:
            print("Can't open file for some reason, check permissions or existance")
            print(error)

    def fuzzer(target, content):
        if arguments.cookiejar != None:
            try:
                for each in self.methodlist:
                    self.methodholder = each
                    for each in self.mimelist:
                        fuzzresult = requests.request(method    = self.methodholder,
                                                        data    = content,
                                                        headers = {'Content-type' : each},
                                                        url     = target,
                                                        cookies = self.cookie)
                        print('status code : ' + upload.status_code)
                        if fuzzresult.status_code == 200:
                            fuzzanalyzer(fuzzresult.content)
                            headersave(fuzzresult.headers)
            except KeyboardInterrupt:
                print('KEYBOARD SIGNALS')
        elif arguments.cookiejar == None:
            try:
                for each in self.methodlist:
                    self.methodholder = each
                    for each in self.mimelist:
                        fuzzresult = requests.request(method    = self.methodholder,
                                                        data    = content,
                                                        headers = self.header.update({'Content-type' : each}),
                                                        url     = target )
                        print('status code : ' + fuzzresult.status_code)
                        if fuzzresult.status_code == 200:
                            fuzzanalyzer(fuzzresult.content)
                            headersave(fuzzresult.headers)
            except KeyboardInterrupt:
                print('KEYBOARD SIGNALS')

    def listener():
        try:
            while True:
                sniff(iface=sniffiface, prn=GET_print, lfilter=lambda p: "GET" in str(p), filter="tcp port 80")
        except:
            print('something happened in the sniffer')

    def headersave(head):
        fileobj = open(self.savefile + time,  "w")
        for each in head:
            print(each, head[each])
            fileobj.append(each, head[each])
    fileobj.close()

    def makesoup(recipie):
        soupymess = BeautifulSoup(recipie , 'lxml')
        #divs = soupyresults.find(lambda tag:  tag.name=='div' and tag.has_key('id') and tag['id'] ==divname)
        #links = soupyresults.find_all(lambda tag:  tag.name=='a' and tag.has_key('alt') and tag['alt'] == 'Magnet Link')
        print(links)
