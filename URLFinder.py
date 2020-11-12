import urllib.request
from bs4 import BeautifulSoup
import re
import json


testIndexUrl = "https://law.emory.edu/ecgar/content/volume-4/issue-special/index.html"


def parseDocument(url):
    page = urllib.request.urlopen(url)
    html = BeautifulSoup(page.read(), "html.parser")

    for link in html.find_all('a'):
        title = link.text
        if "Read More" in title:
            url = link.get('href')
            print(url)

parseDocument(testIndexUrl)
