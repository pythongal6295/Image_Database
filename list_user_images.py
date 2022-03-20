import peewee as pw
import os
import pathlib
import functools
from loguru import logger
from datetime import date

my_basedir = 'C:\\Users\\kelly_kjenkz1\\UW_Python_320A\\Lesson_9\\assignment-09-pythongal6295'


logger.remove()
logger.add('log_' + str(date.today()) + '.log')

use_decorator = True

#logger decorator
def logger_info(func):
    @functools.wraps(func)
    def wrapper_logging(*args, **kwargs):
        value = func(*args, **kwargs)
        logger.info(f'{func.__name__} ran completely.')
        return value
    return wrapper_logging

def do_not_use_decorator(a):
    return a

if not use_decorator:
    logger_info = do_not_use_decorator

@logger_info
def check_length(tags=None):
    '''
    Checks the length of tags are correct.
    user_id does not need to be checked because it was checked 
    when user was added to the database
    user_id: max 30 characters
    tags: max 100 characters
    '''
    if len(tags) > 100:
        return False
    else:
        return True

@logger_info
def picture_id(user_id, picture_table):
    '''
    creates and returns a new picture_id
    '''
    query = picture_table.find(user_id = user_id)
    # for item in query:
    #     print(item)
    pic_id_num = len(query) + 1 

    picture_id = f'{pic_id_num:0>10}'

    return picture_id

@logger_info
def add_picture(picture_id, user_id, tags, picture_table, user_table):
    '''
    Adds a new user to the collection
    '''
    try:
        user_table.insert(user_id=user_id)
    except pw.IntegrityError:
        logger.info(f'User exists: {user_id}')

        len_checker = check_length(tags)
        if len_checker:
            picture_table.insert(picture_id=picture_id,
                        user_id=user_id,
                        tags=tags)
            logger.info("picture successfully added")
            return True
        else:
            logger.info('Tags not of the correct length. ',
                'Picture cannot be added to the database.')
            return False
    else:
        logger.warning(f"Picture not added, missing required foreign key user_id: {user_id}.")
        users_table.delete(user_id)
        return False


@logger_info
def tag_path_formatter(tags):
    '''
    takes string of tags, breaks them up, sorts them, returns a path
    '''
    
    tags = tags.replace('#', '')
    indiv_tags = tags.split(' ')

    indiv_tags.sort()

    return indiv_tags

@logger_info
def image_directory(my_basedir):
    img_dir = my_basedir + '\\images'
    return img_dir


@logger_info
def user_directory(user_id, my_basedir):
    img_dir = image_directory(my_basedir)
    user_id_dir = os.path.join(img_dir, user_id)
    return user_id_dir


@logger_info
def save_picture(picture_id, user_id, indiv_tags, my_basedir):
    '''
    saves a picture to disk with the correct directory format
    '''

    #I can create the folders based on the tags, but not sure how to 
    #save a png file name in that last folder

    img_dir = image_directory(my_basedir)

    path = os.path.join(img_dir, user_id, *indiv_tags)

    print(path)

    directory = pathlib.Path(path)
    directory.mkdir(parents=True, exist_ok=True)

    with open(str(path + f'\\{picture_id}.png'), 'w') as file:
    #with open((str(path + '\\' + '000001.png')), 'w') as file:
        print('Picture saved to disk.')
    
    return True


@logger_info
def list_user_images(user_id, parent_path, dir_lst, tpl_lst):

    if len(dir_lst) == 0:
        return
    else:
        for sub_path in dir_lst:
            full_path = os.path.join(parent_path, sub_path)

            if os.path.isdir(full_path):
                list_user_images(user_id, full_path, os.listdir(full_path), tpl_lst)
            elif os.path.isfile(full_path):
                picture_tpl = (user_id, parent_path, sub_path)
                tpl_lst.append(picture_tpl)

@logger_info
def reconcile_images(user_id, tpl_lst, picture_table):
    db_lst = []
    disk_lst = []

    query = picture_table.find(user_id = user_id)

    for entry in query:
        file_name = entry['picture_id']
        db_lst.append(file_name)

    for entry in tpl_lst:
        file_name = entry[0]
        disk_lst.append(file_name)

    not_in_db = []
    not_in_disk = []

    for picture in db_lst[]:
        if picture not in disk_lst:
            not_in_disk.append(picture)

    print(f'These files are not saved on disk: {not_in_disk}')

    for picture in disk_lst:
        if picture not in db_lst:
            not_in_db.append(picture)

    print(f'These files are not saved in the database: {not_in_db}')

