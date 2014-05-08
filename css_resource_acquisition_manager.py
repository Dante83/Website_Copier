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

resource_url_list = []

#Problems: Create the right file structure

#Turn off annoying error and warning messages from css utilities
#(It doesn't recognize everything it sees, but it still works)
cssutils.log.setLevel(logging.CRITICAL)

def clone_all_css_resources(css, current_directory, root_url, root_directory):
    #Clone all resources associated with each url
    css_sheet = cssutils.parseString(css)
    resource_urls = cssutils.getUrls(css_sheet)

    for url in resource_urls:
        if url not in resource_url_list:
            resource_url_list.append(url)

            #Create any required new directories for this url
            url = urlparse.urljoin(root_url, url)
            css_directory = check_create_directory(url, current_directory, root_directory)

            file_name = urlparse.urlparse(url).path.split('/')[-1]

            #Save this file to the directory
            try:
                output_file_directory = os.path.join(css_directory, file_name)
                urllib.urlretrieve(url, output_file_directory)
            except:
                print 'io error'
                print url
                print output_file_directory
                #raise Exception("UrlLib Error: writing file %s" % os.path.join(css_directory, file_name) )
                sys.exit(0)

            print("%s cloned..." % url)