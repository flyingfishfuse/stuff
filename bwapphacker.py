#!/bin/python
#this is a big playground of experimentation so no its not useable
# I use this with bpython using copy+paste to learn about http

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import urllib
import requests
import argparse
import time
import re
import os

useragent   = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0'}
bwaplogin   = 'http://192.168.0.3/bwapp/login.php'
bwapgetxss  = 'http://192.168.0.3/bwapp/htmli_get.php'
bwappass    = 'bug'
bwapuser    = 'bee'
postparams   = {'login': bwapuser, 'password': bwappass, 'security_level':'0', 'form':'submit'}
typelist = ['name','type','id']
nametype = ['username', 'login']
userfield = None
passfield     = None
userinput = {}
passinput = {}
optionname = {'bug':'2','form':'submit'}
fuzzystring = "FUZZYBUTT" #not a very common phrase, should be ok.
fuzzerregex = re.compile(fuzzystring, re.IGNORECASE|re.DOTALL)
optionlist = []
def seleniumlogin(username,password):
    chromeoptions = Options()
    chromeoptions.add_argument('--headless')
    chromeoptions.binary_location = '/usr/bin/chromium'
    global browser
    browser = webdriver.Chrome(chrome_options=chromeoptions)
    browser.get(bwaplogin)
    asdf = browser.page_source.encode('utf-8')
    soupymess = BeautifulSoup(asdf , 'lxml')
    #inputs = browser.find_elements_by_tag('input')
    if browser.find_elements_by_name('login') != []:
        userinput.update({'login': bwapuser})
        userfield = browser.find_element_by_name('login')
        userfield.send_keys(bwapuser)
    elif browser.find_element_by_name('username') != []:
        userinput.update({'username': bwapuser})
        userfield = browser.find_elements_by_name('username')
        userfield.send_keys(bwapuser)

    if browser.find_elements_by_name('password') != []:
        passinput.update({'password': bwappass})
        passfield = browser.find_element_by_name('password')
        passfield.send_keys(bwappass)
    else:
        print("no password field found?")

def getparams(get):  #AND FUZZ THE CRAP OUT OF THEM <---- bookmark
#call AFTER the global sessions have been started, of course you have no use
#for this function before that ,sooooo....
    return dict(parse.parse_qsl(parse.urlsplit(get).query))

def getreflection():
    input = soupymess.find_all(lambda tag:  tag.name=='input')
    params = soupymess.find_all(lambda tag: tag.name=='input' )
    return input

def selectoptions(htmlbody):
    alloptions = soupymess.find_all(lambda tag:  tag.name=='option' and tag.has_attr('value'))
    for option in alloptions:
        optionlist.append({'value' : option['value']})

def makesoup(htmlbody):
    global soupymess
    soupymess = BeautifulSoup(htmlbody , 'lxml')

def loginrequests(target, username, password):
    global sess
    sess = requests.session()
    sess.get(target, headers= useragent)
    afterlogin = sess.post(url = target , data = postparams) #make the post request
    makesoup(afterlogin.content)
    selectoptions(afterlogin.content)
    inputs = getallinputs()


def getalllinks(html):
    soupymess.find_all(lambda tag:  tag.name=='a' and tag.has_attr('href'))

def getallinputs():
    return soupymess.find_all(lambda tag:  tag.name=='input')

loginrequests(bwaplogin, bwapuser, bwappass)
#def xssinjector():
#    getparams(sess.url)
#    try:
#        with open(macfile , "r") as f:
#            filelines = f.readlines()
#            for eachline in filelines:
