import urllib.request
from bs4 import BeautifulSoup
import re

#testURL = "https://law.emory.edu/elj/content/volume-59/issue-1/index.html"
#testIssueURL = "https://law.emory.edu/elj/content/volume-59/index.html"
testVolumeURL = "https://law.emory.edu/elj/content/index.html"
rootURL = testVolumeURL[:-10]
#rootIssueURL = testIssueURL[:-10]
rootVolumeURL = testVolumeURL[:-10]

#ignore index.html
#<a href="comments/rluipa-rights-religious-same-sex-relationships.html">
#<a href="articles/wikitruth-through-wikiorder.html">

def getURLs(url):
    page = urllib.request.urlopen(url)
    html = BeautifulSoup(page.read(), "html.parser")
    urlList = []
    localRootURL = url[:-10]

    for link in html.find_all('a'):
        potentialURL = link.get('href')
        if "articles" in potentialURL:
            if "index" in potentialURL:
                continue
            if "/articles" in potentialURL:
                continue

            potentialURL = localRootURL + potentialURL
            urlList.append(potentialURL)

        if "comments" in potentialURL:
            if "index" in potentialURL:
                continue
            if "/comments" in potentialURL:
                continue

            potentialURL = localRootURL + potentialURL
            urlList.append(potentialURL)
    return urlList

#getURLs(testURL)

def getIndexURLs(url):
    page = urllib.request.urlopen(url)
    html = BeautifulSoup(page.read(), "html.parser")
    urlList = []
    article = html.find('article')
    for link in article.find_all('a'):
        potentialURL = link.get('href')
        #<a href="issue-2/index.html">
        if "issue" in potentialURL:
            potentialURL = rootIssueURL + potentialURL
            urlList.append(potentialURL)

#getIndexURLs(testIssueURL)
def getVolumeURLs(url):
    page = urllib.request.urlopen(url)
    html = BeautifulSoup(page.read(), "html.parser")
    urlList = []
    article = html.find('article')
    for link in article.find_all('a'):
        potentialURL = link.get('href')
        if "issue" in potentialURL:
            potentialURL = rootVolumeURL + potentialURL
            urlList.append(potentialURL)

    return urlList

volumeURLs = getVolumeURLs(testVolumeURL)
masterURLlist = []
for url in volumeURLs:
    masterURLlist.append(getURLs(url))

for url in masterURLlist:
    print(url)
