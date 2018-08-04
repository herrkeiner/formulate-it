#!/usr/bin/python
import json, mysql.connector as mysqlc
from mysql.connector import errorcode

'''Module for making the connection with the MySQL'''

def load_config(cFileName='config.cfg'):
    ''' Loads database information from the [arg] confirguration file.
        If [arg] isn't specified, then uses the config.cfg file.
        If the file doesn't exists, it creates it and writes dabase information.
    '''
    try:
        f = open(cFileName, 'r')
        config = json.loads(f.read())
        f.close()
        return config
    except FileNotFoundError:
        print('---------- Creating {0} ----------'.format(cFileName))
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
    '''Make a connection with the MySQL database using the dictionary [arg] as the parameters for the connectionself.
        If the connection is successful, returns a MySQL.Connect connector;
    '''
    try:
        print('Connecting to the MySQL server...')
        # Make the connection with the MySQL server
        cHandle = mysqlc.connect(user=config['user'], password=config['password'], host=config['host'])
        # Try to change to the database
        print('Changing database...')
        cHandle.database = config['db']
    except mysqlc.Error as err:
        # The database doesn't exists
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("'{0}' database doesn't exist, creating database...".format(config['db']))
            cursor = cHandle.cursor()
            # Let's create it
            try:
                print('Creating database...')
                cursor.execute("CREATE DATABASE {0} DEFAULT CHARACTER SET 'utf8'".format(config['db']))
                print("'{0}' database has been created successfully!")
            except mysql.Error as err:
                print('Error in the creation of the database!')
                print('Exception info: {0}'.format(err))
                return None
        else:
            print(err)
            return None
    return cHandle

if __name__ == '__main__':
    connect()
