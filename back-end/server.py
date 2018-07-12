#!/usr/bin/python
'''Basic Webserver for formulate-it project'''

import os, sys
from bottle import route, run, static_file, redirect
import math4fun as m4f

# Importing the mff module
sys.path.insert(0, os.path.realpath('assets/'))
os.chdir('../front-end/')


@route('/')
@route('/index.html')
def send_html():
    f = open('index.html')
    data = f.read()
    f.close()
    return data

@route('/static/<filepath:path>')
def send_static(filepath=None):
    return static_file(filepath, root='./static/')

@route('/parser&q=<number:re:\d*>')
def processRequest(number):
    dataDict = dict()
    dataDict['rNumber'] = number
    try:
        dataDict['fResult'] = m4f.primeFact(int(number))
    except ValueError:
        dataDict['fResult'] = 'NaN'

    return str(dataDict)

#@route('/<:re:index.html>')
#def wrong_path():
#    redirect("/index.html")

run(host='localhost', port=8080, debug=True)
