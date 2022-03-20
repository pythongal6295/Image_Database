import os

#empty outbox list
#empty file list
#begin recursion loop
#if file list = 0 then look through parent directory
#check to see if there is a file
    #if yes then add file to file list and return
    #Build the tuple out of user_id, path (minus base directory), file_name

    #if no then add directory info to outbox list
    #continue recursion somehow knowing how to move to the next level...

user_id = 'daisy45'

my_basedir = 'C:\\Users\\kelly_kjenkz1\\UW_Python_320A\\Lesson_9\\assignment-09-pythongal6295'

img_dir = my_basedir + '\\images'

user_id_dir = os.path.join(img_dir, user_id)

tpl_lst = []





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


if __name__ is "__main__":
    if os.listdir(user_id_dir):
        user_id_lst = os.listdir(user_id_dir)
        list_user_images(user_id, user_id_dir, user_id_lst, tpl_lst)

    else:
        print('User_id not found.')

    print(tpl_lst)
