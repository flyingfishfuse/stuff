#!/bin/python
#this is a big playground of experimentation so no its not useable
# I use this with bpython using copy+paste to learn about http

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from selenium import webdriver
from selenium.webdriver.common import keys
from bs4 import BeautifulSoup
import urllib
import requests
import argparse
import time
import re
import os

import colorama
from colorama import init
init()
from colorama import Fore, Back, Style

parser = argparse.ArgumentParser(description='Brute-Force URL fuzz-a-lyzer')
parser.add_argument('--target',
                                 dest    = 'target',
                                 action  = "store" ,
                                 default = 'http:192.168.0.3/bwapp/login.php' ,
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
                                 default =  'login=bee&password=bug&security_level=0&form=submit',
                                 help    = "Data to send through post" )
parser.add_argument('--extraheaders',
                                 dest    = 'extraheaders',
                                 action  = "store" ,
                                 default = None ,
                                 help    = "extra headers, anybody?" )

arguments = parser.parse_args()

#Don't hate on me for using global variables and declaring them at the start
# it's easy to keep track of stuff!
bwaplogin   = 'http://192.168.0.3/bwapp/login.php'
bwappass    = 'bug'
bwapuser    = 'bee'
password    = ('bee','bug')
target      = arguments.target
phpsessid   = ''
header      = {}
postdata    = {}
soupymess   = None
jsonbool    = False
useragent   = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0'}
extraheaders= arguments.extraheaders
fuzzystring = "FUZZYBUTT" #not a very common phrase, should be ok.
fuzzerregex = re.compile(fuzzystring, re.IGNORECASE|re.DOTALL)
inputs      = None
typelist = ['name','type','id']
nametype = ['username', 'login']
userfield = None
passfield     = None

def makeheaders(newheaders):
    headers = header.update(useragent)
    headers.update(newheaders)
    return headers

def requestslogin():
    bwapsession = requests.session()
    fuzz1 = bwapsession.get(url = bwaplogin)
    bwapsession.auth(password)
    #bwapsession.auth(bwapuser:bwapass)

def seleniumgetlogin(url):
    blueprint("Trying to get login with selenium")
    browser = webdriver.phantomjs
    browser.get(url)
    greenprint("Waiting for 10 sec for reply")
    time.sleep(10)
    submit = browser.find_element_by_xpath("//*[@type='submit']")
    passfield = browser.find_element_by_tag_type('password')
    try:
        userfield = browser.find_element_by_name('username')
    except NoSuchElementException:
        userfield = browser.find_element_by_name('login')
    except NoSuchElementException:
        userfield = browser.find_element_by_id('username')
    except NoSuchElementException:
        userfield = browser.find_element_by_id('login')

def getparams(get):  #AND FUZZ THE CRAP OUT OF THEM <---- bookmark
    return dict(parse.parse_qsl(parse.urlsplit(get).query))

def getallinputs():
    input = soupymess.find_all(lambda tag:  tag.name=='input')
    return input

#make a beautiful soup out of this messy html
def getpasswordfield(htmlbody):
    soupymess = BeautifulSoup(htmlbody , 'lxml')
    #and find any inputs, shove em in a box for a handler!
    for each in typelist:
        asdf = makemess('input', each, 'password')
        if asdf != None:
            return asdf

def getusernamefield(htmlbody):
    soupymess = BeautifulSoup(htmlbody , 'lxml')
    holder = None
    for each in typelist:
        holder = each
        for each in nametype:
            asdf = makemess('input', holder, each)
            if asdf != None:
                return asdf
            else:
                pass
    return asdf

def makemess(tag, key, value):
    asdf = soupymess.find_all(lambda tag:  tag.name==tag and tag.has_key(key) and tag[key] == value)
    print(asdf)
    return asdf

def getsubmit(htmlbody):
    soupymess = BeautifulSoup(htmlbody , 'lxml')
    submit = makemess('input','type','submit')
    print(submit)

def checkifjson(urlcontent):
    try:
        urlcontent = req.json()
        return True
    except ValueError:
        urlcontent = req.content
        return False

def blueprint(text):
    print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL)

def greenprint(text):
    print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL)

def redprint(text):
    print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL)


if arguments.postdata == None:
    req = requests.request(method = 'get', url = target ) #make the GET request
    if checkifjson(req.content) is False:
        webpageinput = getinputs(req.content) #SOUPIFY FOR INPUTS!
if arguments.postdata != None:
    postparams = getparams(arguments.postdata)
    req = requests.request(method = 'post', url = target , params = postparams) #make the post request
    if checkifjson(req.content) is False:
        webpageinput = getinputs(req.content) #SOUPIFY FOR INPUTS!
