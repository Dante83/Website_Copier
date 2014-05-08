#!/usr/bin/python
import sys
import urllib
import urlparse
from bs4 import BeautifulSoup
from directory_manager import *

resource_list = []

def get_page_resources(file_depth, page_soup, local_file_path, webpage_cursor, root_directory):

    for resource in page_soup.find_all(src = True):
        #Setup the directories
        current_directory = check_create_directory(resource['src'], local_file_path, root_directory)
        url = urlparse.urljoin(webpage_cursor, resource['src'])

        if url not in resource_list:
            #Download the files to these directories
            file_name = urlparse.urlparse(url).path.split('/')[-1]
            try:
                urllib.urlretrieve(url, os.path.join(current_directory, file_name))
            except:
                raise Exception("urllib error: %s" % url )
                sys.exit(0)

            print("%s cloned..." % url)

            #Add this to the list of resources so that we don't go over it a second time
            resource_list.append(url)

        #Change the soup so that each of the src links are relative and
        #work from this page
        depth_relative_link_slashes = '../' * file_depth
        resource['src'] = depth_relative_link_slashes + resource['src'][1:]

    return page_soup