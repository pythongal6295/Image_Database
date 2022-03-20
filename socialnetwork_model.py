'''
Creates DB tables for the social network model
'''

import os
#import peewee as pw
from loguru import logger
from playhouse.dataset import DataSet

#pylint: disable=R0903, C0103

#filename = ':memory:'

class DbConnectionManager():
    '''context manager for the sql database connection'''
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = DataSet('sqlite:///:memory:')
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()


# def check_database_file(filename):
#     '''
#     Checks if database file exists, if it does the file is deleted
#     '''
#     if os.path.exists(filename):
#         os.remove(filename)
#     return True


# def database_connection(filename):
#     '''
#     Creates a connection to the database
#     '''
#     db = DataSet(f'sqlite:///{filename}')
#     return db



# def create_table(table_name):
#     '''
#     Creates a table to be passed to another function
#     '''
#     with DbConnectionManager() as database:
#         table = database.connection[table_name]
#     return table



def users_columns(users_table):
    '''
    Creates unique columns for the Users DB table
    '''
    users_table.insert(user_id='test')
    users_table.create_index(['user_id'], unique=True)
    users_table.delete(user_id='test')

    users_table.insert(user_name='test')
    users_table.create_index(['user_name'])
    users_table.delete(user_name='test')

    users_table.insert(user_last_name='test')
    users_table.create_index(['user_last_name'])
    users_table.delete(user_last_name='test')

    users_table.insert(user_email='test')
    users_table.create_index(['user_email'])
    users_table.delete(user_email='test')


def status_columns(status_table):
    '''
    Creates unique columns for the Status DB table
    '''
    status_table.insert(status_id='test')
    status_table.create_index(['status_id'], unique=True)
    status_table.delete(status_id='test')

    status_table.insert(user_id='test')
    status_table.create_index(['user_id'])
    status_table.delete(user_id='test')

    status_table.insert(status_text='test')
    status_table.create_index(['status_text'])
    status_table.delete(status_text='test')


def picture_columns(picture_table):
    '''
    Creates unique columns for the Picture DB table
    '''
    #picture_id (PK)
    #user_id(limited to 30)
    # #tags (limited to 100)

    picture_table.insert(picture_id='test')
    picture_table.create_index(['picture_id'], unique=True)
    picture_table.delete(picture_id='test')

    picture_table.insert(user_id='test')
    picture_table.create_index(['user_id'])
    picture_table.delete(picture_id='test')

    picture_table.insert(tags='test')
    picture_table.create_index(['tags'])
    picture_table.delete(tags='test')

# def main(filename):
#     '''
#     Checks if a database exists and connects to the database
#     '''
#     #check_database_file(filename)
#     db = database_connection(filename)
#     return db


#if __name__ == '__main__':
    #main(filename)
