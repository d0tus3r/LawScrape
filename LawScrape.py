import urllib.request
from bs4 import BeautifulSoup
import re
import json

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

#placeholder
def getDocumentType(url):
    urlList = url.split("/")
    document_type = ""
    if urlList[7] == "articles":
        document_type = "article"
    elif urlList[7] == "comments":
        document_type = "comment"
    elif urlList[7] == "articles-essays":
        document_type = ""
    elif urlList[7] == "foreword":
        document_type = "foreword"
    elif "symposium" in urlList[7]:
        document_type = "symposium"
    else:
        document_type = ""

    return document_type

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
    elif urlList[3] == "ebdj":
        journal = "Emory Bankruptcy Developments Journal"
    elif urlList[3] == "ecgar":
        journal = "Emory Corporate Governance and Accountability Review"
    elif urlList[3] == "eilr":
        journal = "Emory International Law Review"
    else:
        journal = ""
    return journal

def getAuthor(author):
    #Daniel B. Rodriguez, Mathew D. McCubbins, Barry R. Weingast
    #check to see if paper has multiple authors
    if author.find(',') != -1:
        multiAuthorList = [x.strip() for x in author.split(',')]
        for authors in range(len(multiAuthorList)):
            author = (getNames(multiAuthorList[authors]))
            return author
    else:
        author = (getNames(author))
        return author


def parseDocument(url):
    page = urllib.request.urlopen(url)
    html = BeautifulSoup(page.read(), "html.parser")
    rootUrl = getRootUrl(url)
    fullTextUrl = ""

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
            fullTextUrl = stripPdfUrl(pdfUrl)
            fullTextUrl = rootUrl + fullTextUrl[:-1]

    volume = getVolume(url)
    issue = getIssue(url)
    journalName = getJournal(url)
    original_url = url
    document_type = getDocumentType(url)
    journal = {'title': title, 'fulltext_url': fullTextUrl, 'abstract': abstract, 'author': author, 'document_type': document_type, 'issue': issue, 'volume': volume, 'journal': journalName, 'first_page': first_page, 'orginal_url': original_url}
    return journal

urlList = getURL()
journalList = []

for url in urlList:
    journal = parseDocument(url)
    journalList.append(journal)

json_object = json.dumps(journalList, indent=4)

with open('articles.json', 'w') as outfile:
    outfile.write(json_object)
