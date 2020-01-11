#!/bin/python3



#http://www.wndu.com/templates/2015_Fullscreen_Radar


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
from absl import app
from absl import flags
import colorama
from colorama import init
import urllib
import requests
import argparse
import time
import sys
import re
import os

init()
FLAGS = flags.FLAGS
flags.DEFINE_boolean("Radar", False , "Opens weather radar in a browser window")
flags.DEFINE_string("Locale", 'neworleans', 'refer to the help for more options, you can put a city name, zip code, airport \
                    code or GPS "/-78.46,106.79". Leave empty and use the "special" option for special options please')


#use `which chromium` or `which chromium-browser` to find your install location
chrome_browser_binary_location	= '/usr/bin/chromium-browser'
useragent                   	= {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0'}
HTML_radar_frame            	= '''<html>
                             		<meta http-equiv="refresh" content="300">
	                              	<frameset>
	                              	<frame src="http://www.wndu.com/weather/radar">
	                              	</frameset>
	                              	</html>'''
live_radar_web_location     = 'http://www.wndu.com/templates/2015_Fullscreen_Radar'
local_forcast_terminal      = 'http://wttr.in/'
local_forcast_locality      = 'neworleans'
cli_forcast_url             = local_forcast_terminal + local_forcast_locality


FORCAST_HELP                = print(requests.request("get" , "https://wttr.in/:help").text)

def get_local_forcast_text():
    #Gets a UTF-8 encoded forcast from a script online, help is available at FORCAST_HELP
    local_weather_forcast = requests.request('get' , cli_forcast_url).text 

def makesoup(htmlbody):
    #the soupy mess is SUPPOSED to get everywhere!
    global soupymess
    soupymess = BeautifulSoup(htmlbody , 'lxml')

def selenium__live_radar():
    chromeoptions = Options()
    chromeoptions.binary_location = chrome_browser_binary_location
    #yeah yeah globals are bad... this one is good!
    global browser
    browser = webdriver.Chrome(chrome_options=chromeoptions)
    # This line makes the browser open and grab the page
    browser.get(live_radar_web_location)

if flags.Radar is True:
    selenium__live_radar()
else print 

if __name__ == '__main__':
  app.run(main)