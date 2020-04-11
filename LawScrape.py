import urllib.request
from bs4 import BeautifulSoup

#All print statements are for proof of concept, will be turned into xml doc upon completion

#open file containing journal urls to parse
def getURL():
    f = open('urls')
    urlList = []
    for line in f:
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
    #open url from list
    page = urllib.request.urlopen(url)
    html = BeautifulSoup(page.read(), "html.parser")
    rootUrl = getRootUrl(url)

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

    getVolumeIssue(url)

    print("Journal")
    journal = getJournal(url)
    print(journal)


urlList = getURL()

for url in urlList:
    parseDocument(url)
