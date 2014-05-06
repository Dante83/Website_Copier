#!/usr/bin/python
import sys
import os
import urllib2
import urlparse
from bs4 import BeautifulSoup
from directory_manager import *

css_url_list = []
js_url_list = []
img_url_list = []
mov_url_list = []

#TODO: CSS Acquisition Method
def acquire_css_files(html, webpage_cursor, local_file_path):
    soup = BeautifulSoup(html)

    #Find all css file locations
    for css_link in soup.find_all('link'):

        #Convert relative link to css file to an absolute link
        href = urlparse.urljoin(webpage_cursor, css_link['href'])

        if href not in css_url_list:
            css_url_list.append(href)

            check_create_directory(href, local_file_path)

            file_name = urlparse.urlparse(href).path.split('/')[-1]
            url_components = urlparse.urlparse(href)
            current_directory = os.path.join(url_components.path, local_file_path)

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
#def acquire_js_files():


#TODO: Page Resource Acquisition Method