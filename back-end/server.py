#!/usr/bin/python
'''Basic Webserver'''

from bottle import route, run, static_file, redirect
import os

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
    if number == '':
        number = 'NaN'
    return str(number)

@route('/<:re:index.html>')
def wrong_path():
    redirect("/index.html")

run(host='localhost', port=8080, debug=True)
