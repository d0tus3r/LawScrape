import urllib.request
from bs4 import BeautifulSoup
from sys import argv

page = urllib.request.urlopen(argv[1])
html = BeautifulSoup(page.read(), "html.parser")

def getVolume(url):
    urlList = url.split("/")
    print (urlList[5].replace("-", " "))
    print (urlList[6].replace("-", " "))

def getRootUrl(url):
    urlList = url.split("/")
    rootUrl = urlList[0] + "/" + urlList[1] + "/" + urlList[2] + "/" + urlList[3] + "/"
    return rootUrl

def stripPdfUrl(url):
    urlList = url.split("/")
    newString = ""
    for x in urlList:
        if x != "..":
            newString.join(x)
            newString = newString + x + "/"
    return newString

rootUrl = getRootUrl(argv[1])

for link in html.find_all('meta'):
   
    if link.get('property') == 'og:title':
        print("Title")
        print(link.get('content'))
        print("")

    if link.get('name') == 'author':
        print("Author")
        print(link.get('content'))
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
        print(rootUrl + newUrl)


getVolume(argv[1])



