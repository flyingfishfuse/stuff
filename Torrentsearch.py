from bs4 import BeautifulSoup
import requests
import os
import lxml
from xpath import dsl as x
from xpath.renderer import to_xpath

parsefile        = True
inputfile        = open('torrentsearchhtml.html', 'r',)
outputlist       = []
magnetlist       = []
resulttableid    = "D"
divname          = 'detName'
numresults       = 10
searchurl        = "https://pirateproxy.live/search/"
searchindex      = '\/1\/99\/0'

def searchinput():
    try:
        input = raw_input("please type your torrent search parameters > ")
    except NameError:
        pass
    return userinput

searchparam      = searchinput()
outputfile       = open(searchparam + 'torrentlist' , 'w')

def makesoup():
    if parsefile == True:
        soupyresults   = BeautifulSoup(inputfile, 'lxml')
    elif parsedfile == False:
        searchresultsweb = requests.get(searchurl + searchparam + searchindex).response.read().decode('utf-8')
        soupyresults   = BeautifulSoup(searchresultsweb.content , 'lxml')
    #extra single quote tag somewhere on every pirate bay mirror
    divs = soupyresults.find(lambda tag:  tag.name=='div' and tag.has_key('id') and tag['id'] ==divname)
    broken = soupyresults.find(lambda tag:  tag.name=='select' and tag.has_key('id') and tag['id'] == 'category')
