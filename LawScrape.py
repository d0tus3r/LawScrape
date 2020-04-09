import urllib.request
from bs4 import BeautifulSoup
from sys import argv

page = urllib.request.urlopen(argv[1])
html = BeautifulSoup(page.read(), "html.parser")

def getVolume(url):
    urlList = url.split("/")
    print (urlList[5].replace("-", " "))
    print (urlList[6].replace("-", " "))

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

getVolume(argv[1])



