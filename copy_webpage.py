#!/usr/bin/python

import Tkinter, tkFileDialog
import sys
import os
import urllib2
from bs4 import BeautifulSoup

#Acquire the webpage url
url = raw_input("Enter the webpage base url to start from: ")

#Acquire the path for the output webpage
root = Tkinter.Tk()
root.withdraw()
file_path = tkFileDialog.askopenfilename()
file_path_cursor = file_path

#TODO: fix up the url so that it's in the right format, even if the user
#enters a short-hand version.

url_list = [url]
uri_list = []

#Initialize the webpage recursion loop
recursive_webpage_cursor(url)

def recursive_webpage_cursor(url_cursor):
    #Record that the present webpage is being tracked
    if url_cursor not in url_list:
        url_list += url_cursor

    #Navigate to the webpage
    soup = BeautifulSoup(url)

    #Determine path extension from webpage root url
    path_ext = os.path.dirname(url_cursor)
    print 'test1: {}', path_ext

    #Create directory structure unless it already exists
    current_directory = os.path.join(path_ext, file_path)
    print 'test2: {}', current_directory

    if not os.path.exists(current_directory):
        os.makedirs(current_directory)

    #Add this webpage to the current directory unless it already exists
    try:
        if soup.name == '':
            html_file = open(current_directory + 'index.html', 'w')
        else:
            html_file = open(current_directory + soup.name + '.html', 'w')
        html_file.write( soup.prettify() )
    except:
        print 'IO Write Error.'
        sys.exit(0)
    finally:
        html_file.close()

    #TODO: Add all resources of this page to their desired directories unless they
    #already exist


    #Report results
    print "{} cloned...", url_cursor

    for link in soup.find_all('a'):
        if link not in url_list:
            recursive_webpage_cursor(link)

#TODO: Complete Resource Automation
#def gather_resources(resource_type):
#    for resource in soup.find_all(resource_type):
#        resource not in uri_list:
#            res = requests.get(resource)
#
#            #Create the resource directory if it doesn't exist

            #Save the resource to this local directory