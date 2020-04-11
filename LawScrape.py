#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
from sys import argv

# Refactor to pull urls from a text document
page = urllib.request.urlopen(argv[1])
html = BeautifulSoup(page.read(), "html.parser")


#open file containing journal urls to parse
def getURL():
    f = open('urls')
    urllist = []
    for line in f:
        print("Parsing url: " + line)
        urlList.append(line)
    return urlList

def getVolumeIssue(url):
    urlList = url.split("/")
    print (urlList[5].replace("-", "\n"))
    print("")
    print (urlList[6].replace("-", "\n"))
    print("")

def getRootUrl(url):
    urlList = url.split("/")
    rootUrl = urlList[0] + "/" + urlList[1] + "/" + urlList[2] + "/" + urlList[3] + "/"
    return rootUrl

def stripPdfUrl(url):
    urlList = url.split("/")
    newString = ""
    for x in urlList:
        if x != "..":
            newString = newString + x + "/"
    return newString

def getTitle(title):
    title = title[0 : (title.find("|") - 1)]
    return title

def getNames(author):
    authorNames = author.split(' ')
    return authorNames

def getAuthor(author):
    #Daniel B. Rodriguez, Mathew D. McCubbins, Barry R. Weingast
    #check to see if paper has multiple authors
    if author.find(',') != -1:
        multiAuthorList = [x.strip() for x in author.split(',')]
        for authors in range(len(multiAuthorList)):
            print(getNames(multiAuthorList[authors]))
    else:
        print(getNames(author))
#continue work on author names


rootUrl = getRootUrl(argv[1])


for link in html.find_all('meta'):

    if link.get('property') == 'og:title':
        print("Title")
        print(getTitle(link.get('content')))
        print("")

    if link.get('name') == 'author':
        print("Author")
        getAuthor(link.get('content'))
        #print(link.get('content'))
        print("")

    if link.get('property') == 'og:description':
        print("Abstract")
        print(link.get('content'))
        print("")

    if link.get('name') == 'start-page-number':
        print("First Page")
        print(link.get('content'))
        print("")

for link in html.find_all('a'):
    pdfUrl = link.get('href')
    if "pdf" in pdfUrl:
        newUrl = stripPdfUrl(pdfUrl)
        print("PDF Url")
        print(rootUrl + newUrl)

print("") #temp line break for readability
#print("Document Type")
#print

getVolumeIssue(argv[1])
