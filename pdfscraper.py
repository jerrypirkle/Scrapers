#!/usr/bin/env python3
"""
Simple PDF Scraper
"""

__author__ = "Jerry Pirkle"
__version__ = "0.1.0"
__license__ = "MIT"

import requests
from bs4 import BeautifulSoup
import os
import re

url =''

# Spoof user agent
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
headers = {'User-Agent': user_agent}
response = requests.get(url,headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

links =  soup.findAll('a')

# enumerate through list of links
for i in links:
    # determine the full url from the site url and the link if the link is using relative file paths
    fullurl = url + i.get('href')
    # find characters tht need to be escaped
    escaped = fullurl.translate(str.maketrans({"-":  r"\-",
                                              "]":  r"\]",
                                              "\\": r"\\",
                                              "^":  r"\^",
                                              "$":  r"\$",
                                              "*":  r"\*",
                                              ".":  r"\.",
                                              "(": r"\(",
                                              ")": r"\)"}))
    # if a link ends with '.pdf', download it
    if fullurl.endswith('.pdf'):
        print('Downloading %s' % fullurl)
        print(re.escape(fullurl))
        os.system('wget %s' % re.escape(fullurl))
