import urllib2, urllib, random, datetime
from lxml import etree
from urlparse import urlparse
from tidylib import tidy_document
url = ''
logfile = 'log.txt'
hostname = urlparse(url).hostname

def validate(html):
    document, errors = tidy_document(html)
    if len(errors) == 0:
        return True
    else: 
        return False
        
def getUrl(url):
    headers = { 'User-Agent': 'HTML validate Bot' }
    req = urllib2.Request(url, '', headers)
    return urllib2.urlopen(req)
    
def extractLinks(html):
    linkList = []
    tree = etree.HTML(html)
    for link in tree.xpath('/html/body//a/@href'):
       linkList.append(link)
    return list(set(linkList))
      
urlList = []
crawledUrls = {}
urlList.append(url)
logfile = open(logfile, 'a')

while len(urlList) !=0:
    url = urlList[random.randrange(0, len(urlList))]
    if not crawledUrls.has_key(url) and urlparse(url).hostname == hostname:
        response = getUrl(url)
        timestamp = str(datetime.datetime.now())
        if response.info().getheader('Content-Type').find("text/html;") != -1:
            html = response.read()
            urlList = urlList + extractLinks(html)
            if validate(html):
                print 'VALID '  + timestamp+ ' : ' + url
                logfile.write('VALID '  + timestamp+ ' : ' + url + '\n')
            else:
                print 'INVALID '  + timestamp+ ' : ' + url
                logfile.write('INVALID '  + timestamp+ ' : ' + url + '\n')
                
        crawledUrls[url]=timestamp
    
    urlList.remove(url)
    
logfile.close()