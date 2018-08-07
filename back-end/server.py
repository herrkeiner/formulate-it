#!/usr/bin/python
'''Basic Webserver for formulate-it project'''
import os, sys, json, mysql.connector
from bottle import route, run, static_file, redirect
import math4fun as m4f
import database_connection as dbcModule

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

    # Verifies if the number's information already exists in the db #
    # Is the querry not a number?
    try:
        number = int(number)
        cnx = dbcModule.connect()
        if cnx:
            cursor = cnx.cursor()
            cursor.execute("SELECT is_prime, is_pali, factorization FROM math_is_fun WHERE id = %s", (number,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                (dataDict['isPrime'], dataDict['isPalin'], dataDict['fResult']) = row
                cnx.close()
                dataDict['fResult'] = json.loads(dataDict['fResult'])
                return json.dumps(dataDict)
        cnx.close()
        # is the number too large to be factorized?
        if len(str(number)) <= 9:
            dataDict['fResult'] = m4f.prime_fact(number)
            # does the query has only one factor and its factor's exponent is 1?
            # Yes! Then It is prime! :D
            if len(dataDict['fResult']) == 1 and list(dataDict['fResult'].values())[0] == 1:
                dataDict['isPrime'] = True
            else: dataDict['isPrime'] = False

            # check if the number is palindromic
            dataDict['isPalin'] = m4f.is_palindromic(number);

            # Record the number information into the database #
            cnx = dbcModule.connect()
            if cnx:
                cursor = cnx.cursor()
                cursor.execute(
                "INSERT INTO math_is_fun (id, is_prime, is_pali, factorization) VALUES (%s, %s, %s, %s)",
                (dataDict['rNumber'], dataDict['isPrime'], dataDict['isPalin'], json.dumps(dataDict['fResult'])))
                cursor.close()
                cnx.commit()
            cnx.close()
        else: dataDict['fResult'] = 'Too large'
    except ValueError:
        dataDict['fResult'] = 'NaN'

    return json.dumps(dataDict)

#@route('/<:re:index.html>')
#def wrong_path():
#    redirect("/index.html")

run(host='localhost', port=8081, debug=True)
