'''
This file stitches together functions from users and user_status objects.
'''
import os
import users
import user_status
import list_user_images as lui
import csv
#import peewee as pw


#pylint: disable=C0103


def load_users(filename, user_collection):
    '''
    Opens a CSV file with user data and
    adds it to the database
    '''
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                #reads the header
                file.readline()
                reader = csv.reader(file)
                for row in reader:
                    users.add_user(user_id=row[0], email=row[3],
                                   user_name=row[1],
                                   user_last_name=row[2],
                                   table=user_collection)
            return True
        except IndexError:
            return False
    else:
        raise FileNotFoundError('File name does not exist.')


def load_status_updates(filename, status_collection, user_collection):
    '''
    Opens a CSV file with user data and
    adds it to the database
    '''
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
            #reads the header
                file.readline()
                reader = csv.reader(file)
                for row in reader:
                    user_status.add_status(status_id=row[0], user_id=row[1],
                                   status_text=row[2],
                                   status_table=status_collection,
                                   user_table=user_collection)
            return True
        except IndexError:
            return False
    else:
        raise FileNotFoundError('File name does not exist.')


def add_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)
    '''
    return users.add_user(user_id, email,
                                user_name, user_last_name, user_collection)


def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user
    '''
    return users.modify_user(user_id, email,
                                user_name, user_last_name, user_collection)


def delete_user(user_id, user_collection, status_collection):
    '''
    Deletes a user from user_collection.
    '''
    return users.delete_user(user_id, user_collection, status_collection)


def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection
    (which is an instance of UserCollection).
    '''
    search_result = users.search_user(user_id, user_collection)
    return search_result


def add_status(status_id, user_id, status_text, status_collection, user_collection):
    '''
    Creates a new instance of UserStatus and stores it in user_collection
    (which is an instance of UserStatusCollection)
    '''
    return user_status.add_status(status_id, user_id, status_text, status_collection, user_collection)


def update_status(status_id, user_id, status_text, status_collection, user_collection):
    '''
    Updates the values of an existing status_id
    '''
    return user_status.modify_status(status_id, user_id, status_text, status_collection, user_collection)


def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.
    '''
    return user_status.delete_status(status_id, status_collection)


def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection
    '''
    search_result = user_status.search_status(status_id, status_collection)
    return search_result

def add_picture(user_id, tags, picture_collection, user_collection):
    '''
    adds a new picture to the database by storing its unique picture_id, the user's id, and tags
    for where the picture is stored on the disk
    '''
    picture_id = lui.picture_id(user_id, picture_collection)

    return lui.add_picture(picture_id, user_id, tags, picture_collection, user_collection)

def tag_path(tags):
    '''
    turns the string of tags into a correct file path
    '''
    return lui.tag_path_formatter(tags)

def save_picture(user_id, indiv_tags, my_basedir, picture_collection):
    '''
    saves a picture to disk
    '''
    picture_id = lui.picture_id(user_id, picture_collection)
    return lui.save_picture(picture_id, user_id, indiv_tags, my_basedir)

def list_user_images(user_id, my_basedir):
    tpl_lst = []
    user_id_dir = lui.user_directory(user_id, my_basedir)

    if os.listdir(user_id_dir):
        user_id_lst = os.listdir(user_id_dir)
        lui.list_user_images(user_id, user_id_dir, user_id_lst, tpl_lst)
        return tpl_lst
    else:
        print('User_id not found.')
        return False
