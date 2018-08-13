#!/usr/bin/python
'''
    Module for making the connection with the MySQL Server.
    It creates the [arg] config file if it doesn't exist.
    It creates the database defined in the config file.
    It creates the math_is_fun table if it doesn't exist.
'''

import json, mysql.connector as mysqlc
from mysql.connector import errorcode
import pdb

def load_config(cFileName='config.cfg'):
    '''
        Loads database information from the [arg] confirguration file.
        If [arg] isn't specified, then uses the config.cfg file.
        If the file doesn't exists, it creates it and writes dabase information.
    '''
    try:
        f = open(cFileName, 'r')
        config = json.loads(f.read())
        f.close()
        return config
    except FileNotFoundError:
        print('---------- Creating {} ----------'.format(cFileName))
        f = open(cFileName, 'x+')
        config = dict()
        config['db'] = input('Type the database name: ')
        config['user'] = input('Type the MySQL user: ')
        config['password'] = input("Type the MySQL user's password: ")
        config['host'] = input('Type the database host: ')
        f.write(json.dumps(config))
        f.close()
        return config

def connect(config=load_config()):
    '''
        Make a connection with the MySQL database using the dictionary [arg] as the parameters for the connection.
        If the connection is successful, returns a MySQL.Connect connector;
    '''
    try:
        # Make the connection with the MySQL server
        cHandle = mysqlc.connect(user=config['user'], password=config['password'], host=config['host'], database=config['db'])
        # Try to change to the database
        cHandle.database = config['db']
    except mysqlc.Error as err:
        # Does the database not exist?
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                cHandle = mysqlc.connect(user=config['user'], password=config['password'], host=config['host'])
                print("'{}' database doesn't exist, creating database...".format(config['db']))
                cursor = cHandle.cursor()
                # Let's create it
                print('Creating database...')
                cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(config['db']))
                print("'{}' database has been created successfully!".format(config['db']))
                #print('Creating table...')
                #print('Table has been created successfully!')
                cursor.close()
                print('Changing database...')
                cHandle.database = config['db']
            except mysql.Error as err:
                print('Exception info: {}'.format(err))
                return None
        else:
            print(err)
            return None
    try:
        cursor = cHandle.cursor()
        cursor.execute("""CREATE TABLE math_is_fun (
                      id INT UNSIGNED NOT NULL AUTO_INCREMENT,
                      is_prime BIT(1) NOT NULL,
                      is_pali BIT(1) NOT NULL,
                      factorization VARCHAR(512),
                      PRIMARY KEY(id))""")
        cursor.close()
        return cHandle
    except mysqlc.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            return cHandle
        else:
            print(err)
            return None

if __name__ == '__main__':
    pass
