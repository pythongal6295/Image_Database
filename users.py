'''
Functions for user information for the
social network project
'''
# pylint: disable=R0903,  E0401
#from datetime import date
from loguru import logger
import peewee as pw

#logger.add('log_' + str(date.today()) + '.log')


def check_length(user_id=None, user_name=None, user_last_name=None):
    '''
    Checks the length of certain pieces of data are correct.
    user_id: max 30 characters
    user_name: max 30 characters
    user_last_name: max 100 characters
    '''
    if len(user_id) > 30:
        return False
    elif len(user_name) > 30:
        return False
    elif len(user_last_name) > 100:
        return False
    else:
        return True

def add_user(user_id, email, user_name, user_last_name, table):
    '''
    Adds a new user to the collection
    '''
    len_checker = check_length(user_id, user_name, user_last_name)
    if len_checker:
        try:
            table.insert(user_id=user_id,
                        user_email=email,
                        user_name=user_name,
                        user_last_name=user_last_name)
            logger.info("User successfully added")
            return True
        except pw.IntegrityError:
            logger.warning("This user already exists.")
            return False
    else:
        logger.info('User data is not of the correct length. ',
            'It cannot be added to the database.')
        return False


def modify_user(user_id, email, user_name, user_last_name, table):
    '''
    Modifies an existing user
    '''
    query = table.find_one(user_id=user_id)
    if query:
        table.update(user_id=user_id, user_email=email,
                    user_name=user_name,
                    user_last_name=user_last_name, columns=['user_id'])
        logger.info("User ID {} modified to have email {},"
                    "first_name {} and last_name {}",
                    user_id, email, user_name, user_last_name)
        return True
    else:
        logger.warning("User cannot be modified as it doesn't exist.")
        return False

def delete_user(user_id, user_table, status_table):
    '''
    Deletes an existing user and all status data
    '''
    query = user_table.find_one(user_id=user_id)
    if query:
        user_table.delete(user_id=user_id)
        logger.info("User_id {} successfully deleted", user_id)
        status_table.delete(user_id=user_id)
        logger.info('User status data for {} also deleted', user_id)
        return True
    else:
        logger.warning("User cannot be deleted as it doesn't exist.")
        return False


def search_user(user_id, table):
    '''
    Searches for user data
    '''
    query = table.find_one(user_id=user_id)
    if query:
        logger.info("User_ID {} found.", user_id)
    else:
        logger.warning("User not found")
    return query
