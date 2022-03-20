'''
Functions for user status information for the
social network project
'''
# pylint: disable=R0903, E0401
from datetime import date
from loguru import logger
import peewee as pw
#import socialnetwork_model as sm

#logger.add('log_' + str(date.today()) + '.log')


def add_status(status_id, user_id, status_text, status_table, user_table):
    '''
    Adds a new user to the collection
    '''
    try:
        user_table.insert(user_id=user_id)
    except pw.IntegrityError:
        logger.info(f'User exists: {user_id}')
        try:
            status_table.insert(status_id=status_id,
                             user_id=user_id,
                             status_text=status_text)
            #logger.info(f"Status successfully added: {status_id}")
            return True
        except pw.IntegrityError:
            logger.warning(f'Status not added, duplicate status ID: {status_id}.')
            return False
    else:
        logger.warning(f"Status not added, missing required foreign key user_id: {user_id}.")
        user_table.delete(user_id=user_id)
        return False


def modify_status(status_id, user_id, status_text, status_table, user_table):
    '''
    Modifies an existing status
    '''
    query = status_table.find_one(status_id=status_id)
    if query:
        try:
            user_table.insert(user_id=user_id)
        except pw.IntegrityError:
            status_table.update(status_id=status_id, user_id=user_id,
                            status_text=status_text, columns=['status_id'])
            logger.info("Status_id {} modified to have user_id {} ",
                        "and status_text {}",
                        status_id, user_id, status_text)
            return True
        else:
            logger.warning("Cannot modify status to a user_id that does not exist.")
            return False
    else:
        logger.warning("Status cannot be modified as it doesn't exist.")
        return False


def delete_status(status_id, status_table):
    '''
    Deletes a user's status data
    '''
    query = status_table.find_one(status_id=status_id)
    if query:
        status_table.delete(status_id=status_id)
        logger.info("Status_id {} successfully deleted", status_id)
        return True
    else:
        logger.warning("Status cannot be deleted as it doesn't exist.")
        return False


def search_status(status_id, status_table):
    '''
    Searches for user status data
    '''
    query = status_table.find_one(status_id=status_id)
    if query:
        logger.info("Status_id {} found.", status_id)
    else:
        logger.warning("Status not found")
    return query
