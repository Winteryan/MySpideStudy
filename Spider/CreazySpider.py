import urllib,gzip
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

def ungzip(data):
    try:
        data = gzip.decompress(data)
    except:
        print("未经压缩，无需解压...")
    return data
# Retrieves a list of all Internal links found on a page
def getInternalLinks(bsObj, includeUrl):
    includeUrl = urllib.parse.urlparse(includeUrl).scheme + "://" + urllib.parse.urlparse(includeUrl).netloc
    internalLinks = []
    # Finds all links that begin with a "/"
    for link in bsObj.findAll("a", href=re.compile("^(/|.*" + includeUrl + ")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if (link.attrs['href'].startswith("/")):
                    internalLinks.append(includeUrl + link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks


# Retrieves a list of all external links found on a page
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    # Finds all links that start with "http" or "www" that do
    # not contain the current URL
    for link in bsObj.findAll("a", href=re.compile("^(http|www)((?!" + excludeUrl + ").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


def getRandomExternalLink(startingPage):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/60.0.3112.113 Safari/537.36'
            # 'Connection': 'keep - alive',
            # 'Upgrade - Insecure - Requests': '1',
            # 'Accept - Language': 'zh - CN, zh;q = 0.8',
            # 'Accept - Encoding': 'gzip, deflate',
            # 'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
            # 'Host': 'blog.csdn.net'
    }
    req = urllib.request.Request(url=startingPage, headers=headers)
    html = urllib.request.urlopen(req)
    data =html.read()
    data = ungzip(data)
    data = data.decode('utf-8')
    # print(data)
    bsObj = BeautifulSoup(data, "html5lib")
    externalLinks = getExternalLinks(bsObj, urllib.parse.urlparse(startingPage).netloc)
    if len(externalLinks) < 10:
        print("没有外链了，再找一个")
        domain = urllib.parse.urlparse(startingPage).scheme + "://" + urllib.parse.urlparse(startingPage).netloc
        print(domain)
        internalLinks = getInternalLinks(bsObj, domain)
        return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]


def followExternalOnly(startingSite):
    print(startingSite)
    print("_________________")
    externalLink = getRandomExternalLink(startingSite)
    print(externalLink)
    print("随机外链为 " + externalLink)
    try:
        print("1")
        followExternalOnly(externalLink)
    except:
        print("2")
        followExternalOnly(getRandomExternalLink(startingSite))


# Collects a list of all external URLs found on the site
allExtLinks = set()
allIntLinks = set()


def getAllExternalLinks(siteUrl):
    req = urllib.request.Request(url=siteUrl)
    html = urllib.request.urlopen(req)
    data = html.read()
    data = ungzip(data)
    data = data.decode('utf-8')
    # print(data)
    bsObj = BeautifulSoup(data, "html5lib")
    domain = urllib.parse.urlparse(siteUrl).scheme + "://" + urllib.parse.urlparse(siteUrl).netloc
    # bsObj = BeautifulSoup(data, "html.parser")
    internalLinks = getInternalLinks(bsObj, domain)
    externalLinks = getExternalLinks(bsObj, domain)

    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)
    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.add(link)
            getAllExternalLinks(link)


followExternalOnly("http://edu.csdn.net/huiyiCourse/series_detail/66")
allIntLinks.add("http://edu.csdn.net/huiyiCourse/series_detail/66")
getAllExternalLinks("http://edu.csdn.net/huiyiCourse/series_detail/66")