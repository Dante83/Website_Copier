#!/usr/bin/python

import Tkinter, tkFileDialog
from copy_webpage import *

#Acquire the web-page url
#url = raw_input("Enter the webpage base url to start from: ")

#Acquire a replacement root for localhost or current web-page name
#rep_root = raw_input("Enter the replacement webpage root: ")

#Acquire the path for the output web-page
#try:
#    root = Tkinter.Tk()
#    root.withdraw()
#    file_path = tkFileDialog.askdirectory()
#except:
#    print 'TKinter Error - No File Directory Detected'

#TODO: fix up the url so that it's in the right format, even if the user
#enters a short-hand version.

#Initialize the web-page recursion loop
recursive_webpage_cursor('http://localhost:3000', '/Users/davidevans/Documents/Code_Panda_Proving_Grounds', 'code-panda.com')