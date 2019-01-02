#!/usr/bin/python
import cgi
import os

pwd           = os.path.abspath('./')
directorylist = os.listdir(pwd)
patharray     = []
counter       = 0

cgitb.enable()  

print('<!DOCTYPE html><html><head><title>Welcome to HACKBISCUITS!</title>')
print("<style type='text/css'>body{width: 35em; margin: 0 auto; font-family: Tahoma, Verdana, Arial, sans-serif; background-color: #D8DBE2; background-image: url('cyberpunk_girl.jpg'); background-size: cover; background-repeat: space;}")


for each in directorylist:
  path = os.path.abspath(each)
  patharray.append(path)
 
for each in patharray:
  print('<a href="' + each + '" title="' + directorylist[counter] + '">' + directorylist[counter] + '</a>')
  counter = counter + 1

  