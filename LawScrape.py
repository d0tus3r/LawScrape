import urllib.request
from bs4 import BeautifulSoup
import re

#open file containing journal urls to parse
def getURL():
    f = open('urls')
    urlList = []
    for line in f:
        urlList.append(line)
    return urlList

def getVolume(url):
    return re.search('volume-([0-9]*)', url).group(1)

def getIssue(url):
    return re.search('issue-([0-9]*)', url).group(1)

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

def getJournal(url):
    urlList = url.split("/")
    if urlList[3] == "elj":
        journal = "Emory Law Journal"
        return journal

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
# Refactor to pull urls from a text document

def parseDocument(url):
    page = urllib.request.urlopen(url)
    html = BeautifulSoup(page.read(), "html.parser")
    rootUrl = getRootUrl(url)

    for link in html.find_all('meta'):

        if link.get('property') == 'og:title':
            title = getTitle(link.get('content'))

        if link.get('name') == 'author':
            author = getAuthor(link.get('content'))

        if link.get('property') == 'og:description':
            abstract = link.get('content')

        if link.get('name') == 'start-page-number':
            first_page = link.get('content')

    for link in html.find_all('a'):
        pdfUrl = link.get('href')
        if "pdf" in pdfUrl:
            newUrl = stripPdfUrl(pdfUrl)
            print("PDF Url")
            print(rootUrl + newUrl)

    volume = getVolume(url)
    issue = getIssue(url)
    journalName = getJournal(url)

    journal = {'title': title, 'journal': journalName, 'abstract': abstract, 'volume': volume, 'issue': issue}
    return journal

urlList = getURL()
#list of dictionary entries for later CSV generation
journalList = []

for url in urlList:
    journal = parseDocument(url)
    journalList.append(journal)

print(journalList)
