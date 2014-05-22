#!/usr/bin/python

import Tkinter, tkFileDialog
from copy_webpage import *

#Acquire the web-page url
#url = raw_input("Enter the webpage base url to start from: ")
url = 'http://localhost:3000/'

#Acquire a replacement root for localhost or current web-page name
#rep_root = raw_input("Enter the replacement webpage root: ")
rep_root = 'http://www.code-panda.com/bhts/pages'

file_path = '/Users/davidevans/Documents/Bhutan-Static-Page'
#Acquire the path for the output web-page
#try:
#    root = Tkinter.Tk()
#    root.withdraw()
#    file_path = tkFileDialog.askdirectory()
#except:
#    print 'TKinter Error - No File Directory Detected'

#Initialize the web-page recursion loop
recursive_webpage_cursor(url, file_path, rep_root, 0, file_path)