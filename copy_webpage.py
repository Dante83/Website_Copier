#!/usr/bin/python
import sys
import os
import urllib2
import urlparse
from bs4 import BeautifulSoup
from resource_acquisition_manager import *
from page_resource_copier import *
from page_resource_copier import *

url_list = []

def recursive_webpage_cursor(url_cursor, file_path, root_replacement, file_depth, root_directory):
    #Record that the present web-page is being tracked
    url_list.append(url_cursor)

    #Acquire http response from url
    request = urllib2.Request(url_cursor)
    url_components = urlparse.urlparse(url_cursor)
    file_name = url_components.path.split('/')[-1]
    root_path = url_components.netloc

    try:
        responce = urllib2.urlopen(request)
        html = responce.read().decode('utf-8', 'ignore')
    except urllib2.URLError, e:
        raise Exception("%s returned an error: %s" % (url_cursor, e) )
        sys.exit(0)

    url_components = urlparse.urlparse(url_components.path)
    current_directory = check_create_directory(url_components.path, file_path, root_directory)

    #Add this web-page to the current directory unless it already exists
    if file_name is '':
        file_loc = os.path.join(current_directory, 'index.html')
    elif file_name.endswith('.html'):
        file_loc = os.path.join(current_directory, file_name)
    else:
        file_loc = os.path.join(current_directory, (file_name + '.html') )

    modified_soup = BeautifulSoup(html)

    #Modify links in file so that they function as relative links in the final
    #output html
    for link in modified_soup.find_all('a'):
        original_link = link['href']

        #Make sure that all absolute path files and the index file use the right
        #web address
        if 'http://' + root_path + '/' == link['href']:
            depth_relative_link_slashes = '../' * file_depth
            updated_link = depth_relative_link_slashes + 'index.html'
        else:
            #Make sure that all non-index files point to html files
            if not link['href'].endswith('.html') and '#' not in link['href']:
                updated_link = link['href'] + '.html'
            else:
                updated_link = link['href']

        #Snip the first forward slash off of relative hyperlinks
        if updated_link.startswith('/'):
            depth_relative_link_slashes = '../' * file_depth
            updated_link = depth_relative_link_slashes + updated_link[1:]

        link['href'] = updated_link

    #Find all css file locations
    for css_link in modified_soup.find_all('link'):
        depth_relative_link_slashes = '../' * file_depth
        updated_link = depth_relative_link_slashes + css_link['href'][1:]

        css_link['href'] = updated_link

    #Acquire all image files
    modified_soup = get_page_resources(file_depth, modified_soup, file_path, url_cursor, root_directory)

    #Check to make sure we're not modifying a link that's already inside
    #of the cloned url list, if so add this link, too.
    if original_link not in url_list:
        url_list.append(updated_link)
        try:
            html_file = open(file_loc, 'w')
            html_file.write( modified_soup.prettify('utf-8'))
        except IOError as e:
            print 'IO Write Error: %s'%e
            sys.exit(0)
        finally:
            html_file.close()

    #Acquire CSS Files
    acquire_css_files(html, modified_soup, url_cursor, file_path, root_directory)

    #Use beautiful soup to iterate over all hyper-links and resources recursively
    soup = BeautifulSoup(html)

    #Report results
    print("%s cloned..." % url_cursor)

    #Find all the hyper-links on this page
    hyperlinks = soup.find_all('a')

    #Filter out all hyper-links which are mailto links
    hyperlinks = filter(lambda link: 'mailto:' not in link['href'], hyperlinks)

    #Filter out bookmark hyper-links
    hyperlinks = filter(lambda link: '#' not in link['href'], hyperlinks)

    #Filter out external hyper-links (e.g. don't copy all of google.com)
    hyperlinks = filter(lambda link: not link['href'].startswith('http://') or link['href'].startswith(url_components.netloc), hyperlinks)

    #Recursively go about traveling through each of these hyper-links repeating
    #this process on those pages that haven't already been created.
    for link in hyperlinks:
        next_page = urlparse.urljoin(url_cursor, link['href'])
        if next_page not in url_list:
            recursive_webpage_cursor(next_page, file_path, root_replacement, next_page.count('/')  - 3, root_directory)