#!/bin/python
import requests
import os
import argparse
from bs4 import BeautifulSoup
import time
import colorama
import re
from colorama import init
init()
from colorama import Fore, Back, Style


#OPTIONS!
parser = argparse.ArgumentParser(description='Brute-Force fuzzer for all methods and options, regexes for a reflection in the response')
parser.add_argument('--file',
                                 dest    = 'file',
                                 action  = "store" ,
                                 default = 'simplebackdoor.php' ,
                                 help    = "The file you are wanting to upload or payload you wish to test" )
parser.add_argument('--cookie',
                                 dest    = 'cookiejar',
                                 action  = "store" ,
                                 default = None ,
                                 help    = "this file is a cookie jar! Only big enough for one cookie! Put a cookie recipie you wish to send along with ... y'know... whatever" )

parser.add_argument('--target',
                                 dest    = 'target',
                                 action  = "store" ,
                                 default = 'http://192.168.1.186' ,
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

header         = {}
savefile       = 'headers : '
url            = arguments.target
xforward       = arguments.xforward
xforwardip     = arguments.xforwardip
useragent      = 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0'
mimetype       = ''
reflectiontag  = 'FUZZYPEACHBUTT'
reflectregex   = re.compile(reflectiontag, re.IGNORECASE|re.DOTALL)
mimelist       = mimelist = ['text/plain',
                                'application/octet-stream',
                                'text/css',
                                'text/html',
                                'text/javascript',
                                'image/gif',
                                'image/jpeg',
                                'image/png',
                                'image/svg-xml']
methodlist     = ['get', 'post','put','head','delete', 'patch','options']
methodholder   = ''

def openfile(filename):
    try:
        fileobject = open(filename, 'rb')
        return fileobject

    except OSError as error:
        print("Can't open file for some reason, check permissions or existance")
        print(error)

fileobj        = openfile(arguments.file)


def main():
    if xforward != None:
        header.update({'X-Forwarded-For' : xforward})
    if xforwardip != None:
        header.update({'X-Forwarded-IP' : xforward})
    if arguments.cookiejar != None:
        cookie = openfile(arguments.cookiejar) #pulling a cookie from the jar!
        print(Fore.RED + cookie + Style.RESET_ALL)

    for each in header:
        print(Fore.RED + each + ' : ' + header[each] + Style.RESET_ALL)
    print(Fore.RED + url + Style.RESET_ALL)
    fuzzer(url, fileobj)

def fuzzer(target, content):
    if arguments.cookiejar != None:
        print(Fore.RED + 'no cookie' + Style.RESET_ALL)
        try:
            for each in methodlist:
                methodholder = each
                for each in mimelist:
                    fuzzresult = requests.request(method    = methodholder,
                                                    data    = content,
                                                    headers = header.update({'Content-type' : each}),
                                                    url     = target,
                                                    cookies = cookie)

                    print(fuzzresult.status_code)
                    if fuzzresult.status_code == 200:
                        #fuzzanalyzer(fuzzresult.content)
                        headersave(fuzzresult.headers)

        except KeyboardInterrupt:
            print(Fore.RED + 'KEYBOARD SIGNALS' + Style.RESET_ALL)

    elif arguments.cookiejar == None:
        print(Fore.RED + 'cookie' + Style.RESET_ALL)
        try:
            for each in methodlist:
                methodholder = each
                for each in mimelist:
                    fuzzresult = requests.request(method    = methodholder,
                                                    data    = content,
                                                    headers = header.update({'Content-type' : each}),
                                                    url     = target )

                    print(fuzzresult.status_code)
                    if fuzzresult.status_code == 200:
                        #fuzzanalyzer(fuzzresult.content)
                        headersave(fuzzresult.headers)

        except KeyboardInterrupt:
            print(Fore.RED + 'KEYBOARD SIGNALS' + Style.RESET_ALL)

def headersave(head):
    fileobj = open(savefile + str(time),  "a")
    for each in head:
        print(each, head[each])
        fileobj.write(each + ' : ' + head[each] + '\n')
    fileobj.close()

def makesoup(recipie):
    soupymess = BeautifulSoup(recipie , 'lxml')
    #divs = soupyresults.find(lambda tag:  tag.name=='div' and tag.has_key('id') and tag['id'] ==divname)
    #links = soupyresults.find_all(lambda tag:  tag.name=='a' and tag.has_key('alt') and tag['alt'] == 'Magnet Link')
    print(links)
    return

if __name__ == '__main__':
    print(Fore.RED + 'main' + Style.RESET_ALL)
    main()
