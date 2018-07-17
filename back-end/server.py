#!/usr/bin/python
'''Basic Webserver for formulate-it project'''

import os, sys, json
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

@route('/parser&q=<number>')
def processRequest(number):
    dataDict = dict()
    # Save the original querry
    dataDict['rNumber'] = number
    # Is the querry not a number?
    try:
        # is the number too large to be factorized?
        if len(str(number)) <= 9:
            dataDict['fResult'] = m4f.primeFact(int(number))
            # does the query has only one factor and its factor's exponent is 1?
            # Yes! Then It is prime! :D
            if len(dataDict['fResult']) == 1 and list(dataDict['fResult'].values())[0] == 1:
                dataDict['isPrime'] = True
            else: dataDict['isPrime'] = False
        else: dataDict['fResult'] = 'Too large'
        # check if the number is palindromic
        dataDict['isPalin'] = m4f.is_palindromic(number);
        print(dataDict['isPalin'])
    except ValueError:
        dataDict['fResult'] = 'NaN'

    return json.dumps(dataDict)

#@route('/<:re:index.html>')
#def wrong_path():
#    redirect("/index.html")

run(host='localhost', port=8080, debug=True)
