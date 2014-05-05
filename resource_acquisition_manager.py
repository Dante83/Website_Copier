#!/usr/bin/python
import sys
import os
import urllib2
import urlparse
from bs4 import BeautifulSoup

css_url_list = []
js_url_list = []
img_url_list = []
mov_url_list = []

#TODO: CSS Acquisition Method
def acquire_css_files(html, webpage_cursor, file_path):
    soup = BeautifulSoup(html)

    #Find all css file locations
    for css_link in soup.find_all('link'):

        #Convert relative link to css file to an absolute link
        href = urlparse.urljoin(webpage_cursor, css_link['href'])

        if href not in css_url_list:
            css_url_list.append(href)

            #Create the directories if they don't exist
            url_components = urlparse.urlparse(href)
            file_name = url_components.path.split('/')[-1]
            current_directory = os.path.join(url_components.path, file_path)
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

            #Save this file to the directory
            request = urllib2.Request(href)
            try:
                responce = urllib2.urlopen(request)
                css = responce.read()
            except urllib2.URLError, e:
                raise Exception("%s returned an error: %s" % (href, e) )
                sys.exit(0)

            #Iterate over all internal resources on each css file
            try:
                if file_name is '':
                    file_loc = os.path.join(current_directory, 'application.css')
                elif file_name.endswith('.css'):
                    file_loc = os.path.join(current_directory, file_name)
                else:
                    file_loc = os.path.join(current_directory, (file_name + '.css') )

                css_file = open(file_loc, 'w')
                css_file.write(css)
            except IOError as e:
                print 'IO Write Error: %s'%e
                sys.exit(0)
            finally:
                css_file.close()

            print("%s cloned..." % href)

            #TODO: Acquire all page resources from this css file

# JavaScript Acquisition Method
def acquire_js_files():


#TODO: Page Resource Acquisition Method