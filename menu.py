'''
Provides a basic frontend
'''
import sys
import main
from loguru import logger
import functools
from datetime import date
import socialnetwork_model as sm
#pylint: disable=C0103

logger.remove()
logger.add('log_' + str(date.today()) + '.log')


use_decorator = True

#logger decorator
def logger_info(func):
    @functools.wraps(func)
    def wrapper_logging(*args, **kwargs):
        value = func(*args, **kwargs)
        logger.info(f'{func.__name__} ran successfully.')
        return value
    return wrapper_logging

def do_not_use_decorator(a):
    return a

if not use_decorator:
    logger_info = do_not_use_decorator


def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    main.load_users(filename, user_collection)
    print('The user data has been loaded.')


def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename, status_collection, user_collection)
    print('The user status data has been loaded.')

@logger_info
def add_user():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id, email, user_name,
                            user_last_name, user_collection):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")


def update_user():
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.update_user(user_id, email, user_name, user_last_name,
                            user_collection):
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")


def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
    if result is None:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result['user_id']}")
        print(f"Email: {result['user_email']}")
        print(f"Name: {result['user_name']}")
        print(f"Last name: {result['user_last_name']}")



def delete_user():
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if not main.delete_user(user_id, user_collection, status_collection):
        print("An error occurred while trying to delete user")
    else:
        print("User and associated status data was successfully deleted")


def add_status():
    '''
    Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(status_id, user_id, status_text,
                                status_collection, user_collection):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")


def update_status():
    '''
    Updates information for an existing status
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text,
                                status_collection, user_collection):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")


def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    user_id = input('user_id ')
    result = main.search_status(status_id, status_collection)
    #query = status_collection.find(user_id=user_id)
    if result is None:
        print("ERROR: Status does not exist")
    else:
        print(f"User ID: {result['user_id']}")
        print(f"Status ID: {result['status_id']}")
        print(f"Status text: {result['status_text']}")
        # print(query)
        # print(len(query))
        # for item in query:
        #     print(item)
        #     print(item['status_text'])
        #print(len(query['status_id']))

def delete_status():
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")

def add_picture():
    '''
    adds a picture's information to the database and asks
    user if they want to save the picture to disk
    '''
    user_id = input('User ID for picture: ')
    tags = input('What tags describe this picture? Space each tag and preface with \'#\'. ')
    if not main.add_picture(user_id, tags, picture_collection, user_collection):
        print('An error occured while trying to add the picture data.')
    else:
        print('Picture data successfully added. Now saving picture to disk.')
        indiv_tags = main.tag_path(tags)
        main.save_picture(user_id, indiv_tags, my_basedir, picture_collection)

def list_user_images():
    '''
    creates a list of file paths and file names for all the images for a user
    '''
    user_id = input('User_id: ')
    return_value = main.list_user_images(user_id, my_basedir)
    if not return_value:
        print('An error occured while trying to retrieve the list.')
    else:
        for tpl in return_value:
            print(tpl, '\n')


def quit_program():
    '''
    Quits program
    '''
    # user_collection.delete()
    # status_collection.delete()
    # db.close()
    sys.exit()


if __name__ == '__main__':

    my_basedir = 'C:\\Users\\kelly_kjenkz1\\UW_Python_320A\\Lesson_9\\assignment-09-pythongal6295'

    with sm.DbConnectionManager() as database:
        user_collection = database.connection['Users']
        sm.users_columns(user_collection)

        status_collection = database.connection['Status']
        sm.status_columns(status_collection)

        picture_collection = database.connection['Picture']
        sm.picture_columns(picture_collection)

    # user_collection = sm.create_table('Users')
    # with sm.DbConnectionManager() as database:
    #     sm.users_columns(user_collection)

    # status_collection = sm.create_table('Status')
    # sm.status_columns(status_collection)

    # db = sm.main('socialnetwork.db')

    # users_tbl = sm.database_tables(db)
    # user_collection = users_tbl('Users')
    # sm.users_columns(user_collection)

    # status_tbl = sm.database_tables(db)
    # status_collection = status_tbl('Users_Status')
    # sm.status_columns(status_collection)

        menu_options = {
            'A': load_users,
            'B': load_status_updates,
            'C': add_user,
            'D': update_user,
            'E': search_user,
            'F': delete_user,
            'G': add_status,
            'H': update_status,
            'I': search_status,
            'J': delete_status,
            'K': add_picture,
            'L': list_user_images,
            'Q': quit_program
        }
        while True:
            user_selection = input("""
                                A: Load user database
                                B: Load status database
                                C: Add user
                                D: Update user
                                E: Search user
                                F: Delete user
                                G: Add status
                                H: Update status
                                I: Search status
                                J: Delete status
                                K: Add picture
                                L: List pictures
                                Q: Quit

                                Please enter your choice: """)
            if user_selection.upper() in menu_options:
                menu_options[user_selection.upper()]()
            else:
                print("Invalid option")
