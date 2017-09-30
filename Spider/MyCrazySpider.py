import urllib,gzip
from bs4 import BeautifulSoup
import re
import datetime
import random

random.seed(datetime.datetime.now())

def saveFile(data):
    path = "F:\\Spider\\myspider.txt"
    file = open(path,'ab')
    for d in data:
        d = str(d)+'\n'
        try:
            file.write(d.encode('gbk'))
        except:
            continue
    # file.encode('utf-8')
    file.close()

def ungzip(data):
    try:
        data = gzip.decompress(data)
    except:
        print("未经压缩，无需解压...")
    return data

def readData(url):
    ret = []
    Links = set()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/60.0.3112.113 Safari/537.36',
        'Connection': 'keep - alive',
        'Upgrade - Insecure - Requests': '1',
        'Accept - Language': 'zh - CN, zh;q = 0.8',
        'Accept - Encoding': 'gzip, deflate',
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        # 'Host': 'www.csdn.net',
        # 'Cache - Control': 'max - age = 0',
        # 'If - Modified - Since': 'Sat, 23 Sep 2017 01:50: 03 GMT',
        # 'If - None - Match': 'W / "59c5bdcb-18356"',
        # 'Upgrade - Insecure - Requests': '1'
    }
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)
    data = res.read()
    data = ungzip(data)
    data = data.decode('utf-8')
    soup = BeautifulSoup(data, 'html5lib')

    for link1 in soup.find_all('a', href=True):
        # for link in link1.find_all(class_="list_item article_item"):
        try:
            t = 'http'
            s = 'https'
            if(t in link1["href"] or s in link1["href"] ):
                print(link1["href"])
                print("#########---来自href---#############")
                ret.append(link1["href"])
                Links.add(link1["href"])
                if(len(Links)==200):
                    saveFile(Links);
                    for x in Links:
                        Links.remove(x)
                    continue
                else:
                    continue
            else:
                for link in soup.find_all('script', src=True):
                    try:
                        t = 'http'
                        s = 'https'
                        if (t in link["src"] or s in link["src"]):
                            print(link["src"])
                            print("##########---来自script---###########")
                            ret.append(link["src"])
                            Links.add(link["src"])
                        else:
                            continue
                    except:
                        continue
        except:
            continue
    try:
        # print("继续找")
        readData(ret[random.randint(0, len(ret) - 1)])
    except:
        # print("出错了，重新找")
        readData(ret[random.randint(0, len(ret) - 1)])

class CSDNSpider:
    def __init__(self,url="http://www.csdn.net"):
        # self.pageIdx = pageIdx
        # self.url = url[0:url.rfind('/')+1]+str(pageIdx)
        self.url=url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/60.0.3112.113 Safari/537.36',
            'Connection': 'keep - alive',
            'Upgrade - Insecure - Requests': '1',
            'Accept - Language': 'zh - CN, zh;q = 0.8',
            'Accept - Encoding': 'gzip, deflate',
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
            # 'Host': 'www.csdn.net',
            # 'Cache - Control': 'max - age = 0',
            # 'If - Modified - Since': 'Sat, 23 Sep 2017 01:50: 03 GMT',
            # 'If - None - Match': 'W / "59c5bdcb-18356"',
            # 'Upgrade - Insecure - Requests': '1'
        }
    def setPages(self,idx):
        self.url = self.url[0:self.url.rfind('/')+1]+str(idx)
    # def readData(self):
    #     ret=[]
    #     str = r'<div.*?article_item">.*?link_title"><a href="(.*?)">(.*?)</a>.*?class="article_description">(.*?)</div>.*?'+\
    #           r'<span class="link_postdate">(.*?)</span>.*?</a>\((.*?)\)</span>.*?'+\
    #           r'</a>.*?\((.*?)\)</span>'
    #
    #     req = urllib.request.Request(url=self.url,headers=self.headers)
    #     res = urllib.request.urlopen(req)
    #
    #     data = res.read()
    #     data = ungzip(data)
    #     data = data.decode('utf-8')
    #     print(data);
    #     pattern = re.compile(str,re.DOTALL)
    #     items = re.findall(pattern,data)
    #     print(items)
    #     for item in items:
    #         ret.append('标题：'+item[1].replace(" ","").strip('\n').replace("space","")
    #                    +'\n链接：http://blog.csdn.net'+item[0]
    #                    +'\n简介:'+item[2].replace(" ","").strip('\n').replace("space","")
    #                    +'\n'+'时间：'+item[3]+'\t阅读：'+item[4]+'\t评论：'+item[5]+'\n'
    #                    +'------------------------------------------------------------------------------------------------------------------------\n')
    #     return ret
    def readData(self):
        ret=[]
        req = urllib.request.Request(url=self.url, headers=self.headers)
        res = urllib.request.urlopen(req)
        data = res.read()
        data = ungzip(data)
        data = data.decode('utf-8')
        soup = BeautifulSoup(data, 'html5lib')
        for link1 in soup.find_all('a',href=True):
            # for link in link1.find_all(class_="list_item article_item"):
            try:
                print(link1["href"])
                print("###################################################")
                ret.append(link1["href"])
            except:
                print("格式错误")
        print("_____________________________________________________")
        for link in soup.find_all(re.compile("<script.*?src=http://.*?</script>")):
            try:
                print(link["src"])
                print("###################################################")
                ret.append(link1["href"])
            except:
                print("格式错误")
        return ret
cs = CSDNSpider()
saveFile(readData("http://www.csdn.com"))
# print(cs.readData())
