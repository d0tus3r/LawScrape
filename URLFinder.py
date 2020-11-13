import urllib.request
from bs4 import BeautifulSoup
import re
import json


testIndexUrl = "https://law.emory.edu/eilr/content/volume-25/issue-1/index.html"
testIndexUrl2 = "https://law.emory.edu/eilr/content/volume-25/issue-2/index.html"
testIndexUrl3 = "https://law.emory.edu/eilr/content/volume-25/issue-3/index.html"


def parseDocument(url):
    page = urllib.request.urlopen(url)
    html = BeautifulSoup(page.read(), "html.parser")

    for link in html.find_all('a'):
        title = link.text
        if "Read More" in title:
            url = link.get('href')
            print("https://law.emory.edu/eilr/content/volume-25/issue-1/"+url)

def parseDocument2(url):
    page = urllib.request.urlopen(url)
    html = BeautifulSoup(page.read(), "html.parser")

    for link in html.find_all('a'):
        title = link.text
        if "Read More" in title:
            url = link.get('href')
            print("https://law.emory.edu/eilr/content/volume-25/issue-2/"+url)


def parseDocument3(url):
    page = urllib.request.urlopen(url)
    html = BeautifulSoup(page.read(), "html.parser")

    for link in html.find_all('a'):
        title = link.text
        if "Read More" in title:
            url = link.get('href')
            print("https://law.emory.edu/eilr/content/volume-25/issue-3/"+url)

parseDocument(testIndexUrl)
parseDocument2(testIndexUrl2)
parseDocument3(testIndexUrl3)
