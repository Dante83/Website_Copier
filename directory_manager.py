#!/usr/bin/python
import os
import urlparse

#Create a new directory if the current directory doesn't exist
def check_create_directory(web_page_directory, local_file_path):
    #Create the directories if they don't exist
    url_components = urlparse.urlparse(web_page_directory)
    current_directory = os.path.join(url_components.path, local_file_path)
    folder_path = url_components.path.split('/')
    del folder_path[-1]

    #Remove empty elements from folder path
    folder_path = filter(None, folder_path)

    #Concatenate all folders in relative local file path
    folder_path_string = ''
    for folder in folder_path:
        folder_path_string = folder + '/' + folder_path_string

    #Create the directory if it doesn't exist
    if folder_path_string is not '':
        current_directory = os.path.join(current_directory, folder_path_string)
        if not os.path.exists(current_directory):
            os.makedirs(current_directory)

    return current_directory