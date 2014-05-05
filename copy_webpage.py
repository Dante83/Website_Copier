#!/usr/bin/python
import sys
import os
import urllib2
import urlparse
from bs4 import BeautifulSoup

url_list = []
uri_list = []
creates_root_index = 0

def recursive_webpage_cursor(url_cursor, file_path, root_replacement):
    #Record that the present webpage is being tracked
    if url_cursor not in url_list:
        url_list.append(url_cursor)

    #Acquire http responce from url
    request = urllib2.Request(url_cursor)

    try:
        responce = urllib2.urlopen(request)
        url_components = urlparse.urlparse(url_cursor)
        file_name = url_components.path.split('/')[-1]
        html = responce.read()

        root_path = url_components.scheme + '://' + url_components.netloc
    except urllib2.URLError, e:
        raise Exception("%s returned an error: %s" % (url_cursor, e) )

    print 'test1: %s' % (file_name)

    #Determine path extension from webpage root url
    print 'test2: ', url_components

    current_directory = os.path.join(url_components.path, file_path)
    print 'test3: ', current_directory

    #Remove the file name from the directory path
    folder_path = url_components.path.split('/')
    del folder_path[-1]

    #Remove empty elements from folder path
    folder_path = filter(None, folder_path)

    #Concatonate all folders in relative local file path
    folder_path_string = ''
    for folder in folder_path:
        folder_path_string = folder + '/' + folder_path_string

    #Create the directory if it doesn't exist
    if folder_path_string is not '':
        current_directory = os.path.join(current_directory, folder_path_string)
        if not os.path.exists(current_directory):
            os.makedirs(current_directory)

    #Add this webpage to the current directory unless it already exists
    try:
        if file_name is '':
            file_loc = os.path.join(current_directory, 'index.html')
            creates_root_index = 1
        elif file_name.endswith('.html'):
            file_loc = os.path.join(current_directory, file_name)
        else:
            file_loc = os.path.join(current_directory, (file_name + '.html') )

        modified_soup = BeautifulSoup(html)

        #for link in modified_soup.find_all('a'):
        #    if (root_path) in link['href']:
        #        link['href'].replace(root_replacement)
                #TODO: Possibly worry about links to the newly created index page
                #if urlparse.urlparse(link['href']).path.split('/')[-1] is '':
                #    link['href'].

        html_file = open(file_loc, 'w')
        html_file.write( modified_soup.prettify("utf-8") )
    except:
        print 'IO Write Error.'
        sys.exit(0)
    finally:
        html_file.close()

    #Use beautiful soup to iterate over all hyperlinks and resources recursively
    soup = BeautifulSoup(html)

    #TODO: Add all resources of this page to their desired directories unless they
    #already exist

    #Report results
    print "{} cloned...", url_cursor

    #Find all the hyper-links on this page
    hyperlinks = soup.find_all('a')

    #Filter out all hyper-links which are mailto links
    hyperlinks = filter(lambda link: 'mailto:' not in link, hyperlinks)

    #Recursively go about traveling through each of these hyper-links repeating
    #this process on those pages that haven't already been created.
    for link in hyperlinks:

        next_page = urlparse.urljoin(url_cursor, link['href'])
        if next_page not in url_list:

            recursive_webpage_cursor(next_page, file_path, root_replacement)

#TODO: Complete Resource Automation
#def gather_resources(resource_type):
#    for resource in soup.find_all(resource_type):
#        resource not in uri_list:
#            res = requests.get(resource)
#
#            #Create the resource directory if it doesn't exist

            #Save the resource to this local directory