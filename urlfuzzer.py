#!/bin/python
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

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
parser = argparse.ArgumentParser(description='Brute-Force URL fuzz-a-lyzer')

parser.add_argument('--target',
                                 dest    = 'target',
                                 action  = "store" ,
                                 default = 'http://127.0.0.1/hack/index.php?page=repeater.php' ,
                                 help    = "TARGET to attack, Don't forget the http://" )
parser.add_argument('--cookie',
                                 dest    = 'cookiejar',
                                 action  = "store" ,
                                 default = None ,
                                 help    = "this file is a cookie jar! Only big enough for one cookie! Put a cookie recipie you wish to send along with ... y'know... whatever" )
parser.add_argument('--method',
                                 dest    = 'method',
                                 action  = "store" ,
                                 default = None ,
                                 help    = "the http method you wanna use" )
parser.add_argument('--postdata',
                                 dest    = 'postdata',
                                 action  = "store" ,
                                 default = None ,
                                 help    = "Data to send through post" )

arguments = parser.parse_args()

target      = arguments.target
phpsessid   = ''
header      = {}
postdata    = {}
jsonbool    = False
useragent   = 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0'
fuzzystring = "FUZZYBUTT" #not a very common phrase, should be ok.
fuzzerregex = re.compile(fuzzystring, re.IGNORECASE|re.DOTALL)

def geturlparams(url):
    params = urlparse(url)

def checkifjson(urlcontent):
    try:
        urlcontent = req.json()
        return True
    except ValueError:
        urlcontent = req.content
        return False

#make a beautiful soup out of this messy html
def getinputs(htmlbody):
    soupymess = BeautifulSoup(htmlbody , 'lxml')
    #and find any inputs, shove em in a box for a handler!
    input = soupymess.find(lambda tag:  tag.name=='input')
    #submit = soupyresults.find_all(lambda tag:  tag.name=='submit' and tag.has_key('type') and tag['type'] == 'submit')
    return input

def getsubmit(htmlbody):


#if we are NOT making a POST request/upload
if arguments.postdata != None:
    req = requests.request(method = 'get', url = target ) #make the GET request
    if checkifjson(req.content) is False:
        webpageinput = getinputs(req.content) #SOUPIFY FOR INPUTS!


def getinputsjson(jsondata):

reflection = fuzzyregex.search()
