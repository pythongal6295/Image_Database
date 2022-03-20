'''
The suite of unit tests for main.py, user_status.py, and users.py
'''
import os
from unittest import TestCase
import mock
import os
import peewee as pw
from playhouse.dataset import DataSet
import socialnetwork_model as sm
import main
import pytest

#pylint: disable=C0103
test_user_data = [('daisy45', 'daisy@gmail.com', 'Daisy', 'Johnson'), 
                     ('jemma32', 'science@outlook.com', 'Jemma', 'Simmons'),
                     ('deke22', 'deke@aol.com', 'Deke', 'Smith'),]

test_status_data = [
            ('daisy45_0001', 'daisy45', 'Fighting bad guys'),
            ('jemma32_0001', 'jemma32', 'Doing some science experiments'),
            ('deke22_0001', 'deke22', 'Welcome to the Lighthouse'),
            ('coulson_0001', 'coulson_19', 'Man of many lives')]

user_filename = 'accounts2.csv'
status_filename = 'status_updates2.csv'


class UsersTests(TestCase):

    def setUp(self):
        self.db = DataSet('sqlite:///:memory:')

        user_collection = self.db['Users']
        sm.users_columns(user_collection)
        self.users = user_collection

        self.user_info = test_user_data

        for user in self.user_info:
            self.users.insert(user_id = user[0], user_email = user[1], user_name = user[2],
                              user_last_name = user[3])

        
        status_collection = self.db['Users_Status']
        sm.status_columns(status_collection)
        self.status = status_collection

        self.status_info = test_status_data

        for status in self.status_info:
            self.status.insert(status_id=status[0], user_id=status[1], status_text=status[2])

    def tearDown(self):
        self.users.delete()
        self.status.delete()
        self.db.close()

    def test_load_users(self):
        '''
        tests user data can be loaded from a csv file
        '''
        return_value = main.load_users(user_filename, self.users)

        new_user = main.search_user(user_id = 'keri42', user_collection=self.users)

        assert new_user['user_id'] == 'keri42'
        assert new_user['user_email'] == 'ks@yahoo.com'
        assert new_user['user_name'] == 'Keri'
        assert new_user['user_last_name'] == 'Smith'
        assert return_value is True

    def test_load_users_file_error(self):
        '''
        tests an incorrect filename is handled appropriately
        '''
        with pytest.raises(FileNotFoundError):
            main.load_users('test.csv', self.users)

    def test_add_new_user(self):
        '''
        tests a new user and its data is added to the database
        '''

        return_value = main.add_user(user_id='fitz20', email='lfitz@yahoo.com', user_name='Leopold', 
                          user_last_name='Fitz', user_collection=self.users)

        new_user = self.users.find_one(user_id = 'fitz20')

        assert new_user['user_id'] == 'fitz20'
        assert new_user['user_email'] == 'lfitz@yahoo.com'
        assert new_user['user_name'] == 'Leopold'
        assert new_user['user_last_name'] == 'Fitz'
        assert return_value is True

    def test_add_current_user(self):
        '''
        tests that a user that already exists is not re-added to the database
        '''
        return_value = main.add_user(user_id='daisy45', email='daisy@gmail.com', user_name='Daisy',
                      user_last_name='Johnson', user_collection=self.users)

        assert return_value is False

    def test_length_checker_user_id(self):
        '''ensures the character limit of 30 characters for the user_id
        is enforced.
        '''
        #Can use a mock for length_checker input to make sure add_user returns False
        #Probably need three of these tests

        return_value = main.add_user(user_id='todd32_000000000000000000000000', email='todd@aol.com',
            user_name='Todd', user_last_name='Smith', user_collection=self.users)

        assert return_value is False

    def test_length_checker_user_name(self):
        '''ensures the character limit of 30 characters for the user_name 
        is enforced.
        '''
        return_value = main.add_user(user_id='todd32', email='todd@aol.com', user_name='Todd_00000000000000000000000000',
            user_last_name='Smith', user_collection=self.users)

        assert return_value is False

    def test_length_checker_user_last_name(self):
        '''ensures the character limit of 100 characters for the user_last_name 
        is enforced.
        '''
        user_last_name = 'Smith_' + ('0' * 95)
        return_value = main.add_user(user_id='todd32', email='todd@aol.com', user_name='Todd', user_last_name=user_last_name,
            user_collection=self.users)

        assert return_value is False

    def test_search_user(self):
        '''
        tests an added user can be searched and returned
        '''
        query = main.search_user('daisy45', user_collection=self.users)

        assert query['user_id'] == 'daisy45'
        assert query['user_email'] == 'daisy@gmail.com'
        assert query['user_name'] == 'Daisy'
        assert query['user_last_name'] == 'Johnson'

    def test_search_nonexistent_user(self):
        '''tests a user not in the database cannot be found when searched
        '''
        query = main.search_user('test_10', user_collection=self.users)

        assert query is None

    def test_modify_user(self):
        '''
        tests a user's information is correctly modified
        '''

        return_value = main.update_user(user_id='jemma32', email='jsimmons@live.com', user_name='J',
                         user_last_name='S', user_collection=self.users)

        updated_user = self.users.find_one(user_id='jemma32')

        print(updated_user)

        assert return_value is True
        assert updated_user['user_id'] == 'jemma32'
        assert updated_user['user_email'] == 'jsimmons@live.com'
        assert updated_user['user_name'] == 'J'
        assert updated_user['user_last_name'] == 'S'

    def test_modify_nonexistant_user(self):
        '''
        tests that a non-existant user is not modified and the function return False
        '''
        return_value = main.update_user(user_id='test_20', email='test_20@gmail.com', user_name='test',
                     user_last_name='test_', user_collection=self.users)

        assert return_value is False

    def test_delete_user(self):
        '''
        tests a user and its associated data is deleted
        '''
        return_value = main.delete_user(user_id='deke22', user_collection=self.users, status_collection=self.status)

        deleted_user = self.users.find_one(user_id='deke22')
        deleted_statuses = self.status.find_one(status_id='deke22_0001')

        assert deleted_user is None
        assert return_value is True
        assert deleted_statuses is None

    def test_delete_nonexistant_user(self):
        '''
        tests that the function recoginizes a non-existant user and returns False
        '''
        return_value = main.delete_user(user_id='test_30', user_collection=self.users, status_collection=self.status)

        assert return_value is False

class StatusTests(TestCase):

    def setUp(self):
        self.db = DataSet('sqlite:///:memory:')

        user_collection = self.db['Users']
        sm.users_columns(user_collection)
        self.users = user_collection

        self.user_info = test_user_data

        for user in self.user_info:
            self.users.insert(user_id = user[0], user_email = user[1], user_name = user[2],
                              user_last_name = user[3])

        status_collection = self.db['Users_Status']
        sm.status_columns(status_collection)
        self.status = status_collection

        self.status_info = test_status_data

        for status in self.status_info:
            self.status.insert(status_id = status[0], user_id = status[1], status_text = status[2])

    def tearDown(self):
        self.users.delete()
        self.status.delete()
        self.db.close()

    def test_load_status_updates(self):
        '''
        tests status data can be loaded from a csv file
        '''
        main.load_users(user_filename, self.users)
        return_value = main.load_status_updates(status_filename, self.status, self.users)

        new_status = main.search_status(status_id = 'keri42_00001', status_collection=self.status)

        assert new_status['user_id'] == 'keri42'
        assert new_status['status_id'] == 'keri42_00001'
        assert new_status['status_text'] == 'Reading a book'
        assert return_value is True

    def test_load_status_file_error(self):
        '''
        tests an incorrect filename is handled appropriately
        '''
        with pytest.raises(FileNotFoundError):
            main.load_status_updates('test.csv', self.status, self.users)

    def test_add_status(self):
        '''
        tests a new status_id and its data is added to the database
        '''

        return_value = main.add_status(status_id='daisy45_0002', user_id='daisy45', status_text='My team has got my back', 
            status_collection=self.status, user_collection=self.users)

        new_status = self.status.find_one(status_id = 'daisy45_0002')

        assert new_status['user_id'] == 'daisy45'
        assert new_status['status_id'] == 'daisy45_0002'
        assert new_status['status_text'] == 'My team has got my back'
        assert return_value is True

    def test_add_current_status(self):
        '''
        tests that a status_id that already exists is not re-added to the database
        '''
        return_value = main.add_status(status_id='daisy45_0001', user_id='daisy45', status_text='Fighting bad guys', 
            status_collection=self.status, user_collection=self.users)

        assert return_value is False

    def test_add_status_nonexistant_user_id(self):
        '''
        tests that a status_id with a non_existant user_id is not added to the database
        '''
        return_value = main.add_status(status_id='daisy45_0001', user_id='test_35', status_text='Just chillin', 
            status_collection=self.status, user_collection=self.users)

        assert return_value is False

    def test_search_status(self):
        '''
        tests an added status can be searched and returned
        '''
        query = main.search_status('daisy45_0001', status_collection=self.status)

        assert query['user_id'] == 'daisy45'
        assert query['status_id'] == 'daisy45_0001'
        assert query['status_text'] == 'Fighting bad guys'


    def test_search_nonexistent_status(self):
        '''tests a user status not in the database cannot be found when searched
        '''
        query = main.search_status('test_status_10', status_collection=self.status)

        assert query is None

    def test_modify_status(self):
        '''
        tests a user's status information is correctly modified
        '''

        return_value = main.update_status(status_id='jemma32_0001', user_id='jemma32', 
            status_text='Why am I always in danger?', status_collection=self.status, user_collection=self.users)

        updated_status = self.status.find_one(status_id='jemma32_0001')

        assert return_value is True
        assert updated_status['user_id'] == 'jemma32'
        assert updated_status['status_id'] == 'jemma32_0001'
        assert updated_status['status_text'] == 'Why am I always in danger?'

    def test_modify_nonexistant_status(self):
        '''
        tests that a non-existant status_id is not modified and the function return False
        '''
        return_value = main.update_status(status_id='test_status_20', user_id='jemma32', 
            status_text='Where is Fitz?', status_collection=self.status, user_collection=self.users)

        assert return_value is False

    def test_modify_status_nonexistant_user_id(self):
        '''
        tests that a status_id in the database is not modified with a non-exsistant user_id
        and the function return False
        '''
        return_value = main.update_status(status_id='jemma32_0001', user_id='test_40', 
            status_text='Stay Calm', status_collection=self.status, user_collection=self.users)

        assert return_value is False

    def test_delete_status(self):
        '''
        tests a status_id and its associated data is deleted
        '''
        return_value = main.delete_status(status_id='deke22_0001',status_collection=self.status)

        deleted_statuses = self.status.find_one(status_id='deke22_0001')

        assert return_value is True
        assert deleted_statuses is None

    def test_delete_nonexistant_status(self):
        '''
        tests that the function recoginizes a non-existant status_id and returns False
        '''
        return_value = main.delete_status(status_id='test_status_30', status_collection=self.status)
        
        assert return_value is False

class PictureTests(TestCase):

    def setUp(self):
        self.db = DataSet('sqlite:///:memory:')

        user_collection = self.db['Users']
        sm.users_columns(user_collection)
        self.users = user_collection

        self.user_info = test_user_data

        for user in self.user_info:
            self.users.insert(user_id = user[0], user_email = user[1], user_name = user[2],
                              user_last_name = user[3])

        picture_collection = self.db['Picture']
        sm.picture_columns(picture_collection)
        self.picture = picture_collection

    def tearDown(self):
        self.users.delete()
        self.picture.delete()
        self.db.close()

    def test_add_picture(self):
        '''tests a picture's data is added to the database
        '''

        return_value = main.add_picture(user_id='daisy45', tags='#fighting #Zephyr', 
            picture_collection=self.picture, user_collection=self.users)

        new_pic = self.picture.find_one(user_id = 'daisy45')

        assert new_pic['user_id'] == 'daisy45'
        assert new_pic['picture_id'] == '0000000001'
        assert new_pic['tags'] == '#fighting #Zephyr'
        assert return_value is True

    def test_add_picture_multiple_pics(self):
        '''tests that add_picture can increment the picture_id by one for each 
        additional picture saved for a user
        '''
        main.add_picture(user_id='daisy45', tags='#badguys #inhuman', 
            picture_collection=self.picture, user_collection=self.users)

        main.add_picture(user_id='daisy45', tags='#friends #family', 
            picture_collection=self.picture, user_collection=self.users)

        main.add_picture(user_id='daisy45', tags='#badguys #Zephyr', 
            picture_collection=self.picture, user_collection=self.users)

        query = self.picture.find(user_id = 'daisy45')

        new_pic_1 = query[0]
        new_pic_2 = query[1]
        new_pic_3 = query[2]

        assert new_pic_1['picture_id'] == '0000000001'
        assert new_pic_2['picture_id'] == '0000000002'
        assert new_pic_3['picture_id'] == '0000000003'

    def test_add_picture_nonexistant_user_id(self):
        '''
        tests that a picture with a non_existant user_id is not added to the database
        '''
        return_value = main.add_picture(user_id='test_11', tags='#badguys #inhuman', 
            picture_collection=self.picture, user_collection=self.users)

        assert return_value is False

    def test_length_checker_tags(self):
        '''ensures the character limit of 30 characters for the user_id
        is enforced.
        '''
        tags = '#surfing' + ('0' * 95)

        return_value = main.add_picture(user_id='daisy45', tags=tags, picture_collection=self.picture, user_collection=self.users)

        assert return_value is False

    def test_tag_path_formatter(self): 
        '''
        ensures the file path for each picture is formatted correctly
        '''
        tag_lst = main.tag_path(tags='#saturday #cars #adventure')

        #assert tag_lst == '\\adventure\\cars\\saturday'
        assert tag_lst == ['adventure', 'cars', 'saturday']


    #Not sure how to do this test....
    def test_save_picture(self):
        '''
        tests a picture is saved to the correct directory on disk
        '''
        tag_lst = main.tag_path(tags='#saturday #cars #adventure')

        path = os.path.join('daiey45', *tag_lst)

        print(path)

        main.save_picture('daisy45', tag_lst)

        #This isn't right
        assert os.path.exists('000001.png')