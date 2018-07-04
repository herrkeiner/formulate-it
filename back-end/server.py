#!/usr/bin/python

from bottle import route, run, static_file
import os

os.chdir('../front-end/')

@route('/')
@route('index.html')
def send_html(filepath='index.html'):
    f = open("./" + filepath)
    data = f.read()
    f.close()
    return data

@route('/static/<filepath:path>')
def send_static(filepath=None):
    return static_file(filepath, root='./static/')

run(host='localhost', port=8080, debug=True)
