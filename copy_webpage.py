#!/usr/bin/python
import sys
import os
import urllib2
import urlparse
import codecs
from bs4 import BeautifulSoup
from resource_acquisition_manager import *

url_list = []

def recursive_webpage_cursor(url_cursor, file_path, root_replacement):
    #Record that the present web-page is being tracked
    if url_cursor not in url_list:
        url_list.append(url_cursor)

    #Acquire http response from url
    request = urllib2.Request(url_cursor)
    url_components = urlparse.urlparse(url_cursor)
    file_name = url_components.path.split('/')[-1]
    root_path = url_components.netloc

    try:
        responce = urllib2.urlopen(request)
        html = responce.read()
    except urllib2.URLError, e:
        raise Exception("%s returned an error: %s" % (url_cursor, e) )
        sys.exit(0)

    #Determine path extension from web-page root url
    current_directory = os.path.join(url_components.path, file_path)

    #Remove the file name from the directory path
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

    #Add this web-page to the current directory unless it already exists
    if file_name is '':
        file_loc = os.path.join(current_directory, 'index.html')
    elif file_name.endswith('.html'):
        file_loc = os.path.join(current_directory, file_name)
    else:
        file_loc = os.path.join(current_directory, (file_name + '.html') )

    modified_soup = BeautifulSoup(html.decode('utf-8'))

    for link in modified_soup.find_all('a'):
        if (root_path) in link['href']:
            updated_link = link['href'].replace(root_path, root_replacement)
        elif not link['href'].endswith('.html'):
            link['href'] += '.html'

        #Check to make sure we're not modifying a link that's already inside
        #of the cloned url list, if so add this link, too.
        if link['href'] in url_list:
            url_list.append(updated_link)
            link['href'] = updated_link

        try:
            html_file = codecs.open(file_loc, 'w', 'utf-8')
            html_file.write( html.decode('utf-8'))
        except IOError as e:
            print 'IO Write Error: %s'%e
            sys.exit(0)
        finally:
            html_file.close()

    #Acquire CSS Files
    acquire_css_files(html, url_cursor, file_path)

    #TODO: Acquire JavaScript Files

    #Use beautiful soup to iterate over all hyper-links and resources recursively
    soup = BeautifulSoup(html)

    #TODO: Acquire Page Resources

    #Report results
    print("%s cloned..." % url_cursor)

    #Find all the hyper-links on this page
    hyperlinks = soup.find_all('a')

    #Filter out all hyper-links which are mailto links
    hyperlinks = filter(lambda link: 'mailto:' not in link['href'], hyperlinks)

    #Filter out bookmark hyper-links
    hyperlinks = filter(lambda link: '#' not in link['href'], hyperlinks)

    #Filter out external hyper-links (e.g. don't copy all of google.com)
    hyperlinks = filter(lambda link: link['href'].startswith('/') or link['href'].startswith(url_components.netloc), hyperlinks)

    #Recursively go about traveling through each of these hyper-links repeating
    #this process on those pages that haven't already been created.
    for link in hyperlinks:
        next_page = urlparse.urljoin(url_cursor, link['href'])
        if next_page not in url_list:
            recursive_webpage_cursor(next_page, file_path, root_replacement)