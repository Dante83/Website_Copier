#!/usr/bin/python
import sys
import os
import urllib
import urllib2
import urlparse
import cssutils
import logging
from bs4 import BeautifulSoup
from directory_manager import *

css_url_list = []
resource_url_list = []

#Turn off annoying error and warning messages from css utilities
#(It doesn't recognize everything it sees, but it still works)
cssutils.log.setLevel(logging.CRITICAL)

#TODO: CSS Acquisition Method
def acquire_css_files(html, webpage_cursor, local_file_path):
    soup = BeautifulSoup(html)

    #Find all css file locations
    for css_link in soup.find_all('link'):

        #Convert relative link to css file to an absolute link
        href = urlparse.urljoin(webpage_cursor, css_link['href'])

        if href not in css_url_list:
            css_url_list.append(href)

            current_directory = check_create_directory(href, local_file_path)
            file_name = urlparse.urlparse(href).path.split('/')[-1]

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

            css_sheet = cssutils.parseString(css)
            resource_urls = cssutils.getUrls(css_sheet)

            for url in resource_urls:
                if url not in resource_url_list:
                    resource_url_list.append(url)

                    #Create any required new directories for this url
                    current_directory = check_create_directory(url, local_file_path)

                    url = urlparse.urljoin(webpage_cursor, url)
                    file_name = urlparse.urlparse(url).path.split('/')[-1]

                    #Save this file to the directory
                    try:
                        urllib.urlretrieve(url, os.path.join(current_directory, file_name))
                    except urllib2.URLError, e:
                        raise Exception("%s returned an error: %s" % (href, e) )
                        sys.exit(0)

                    print("%s cloned..." % url)