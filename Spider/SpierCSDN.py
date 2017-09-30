import urllib.request,re,time,random,gzip
from bs4 import  BeautifulSoup

def saveFile(data,i):
    path = "F:\\Spider\\05_csdn\\papers\\paper_"+str(i+1)+".txt"
    file = open(path,'wb')
    page = '当前页：'+str(i+1)+'\n'
    file.write(page.encode('gbk'))

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

def setData(link):
    href = link.find("span", class_="link_title").find("a", href=True)["href"]
    print(link.find("span", class_="link_title").find("a", href=True)["href"])
    title = link.find("span", class_="link_title").find("a", href=True).get_text()
    print(link.find("span", class_="link_title").find("a", href=True).get_text())
    desc = link.find("div", class_="article_description").get_text()
    print(link.find("div", class_="article_description").get_text())
    date = link.find("span", class_="link_postdate").get_text()
    print(link.find("span", class_="link_postdate").get_text())
    view = link.find("span", class_="link_view").get_text()
    print(link.find("span", class_="link_view").get_text())
    comment = link.find("span", class_="link_comments").get_text()
    print(link.find("span", class_="link_comments").get_text())
    ret='标题：' + title+ '\n链接：http://blog.csdn.net' + href+ '\n简介:' + desc+ '\n' + '时间：' + date + '\t' + view + '\t' + comment + '\n'+ '------------------------------------------------------------------------------------------------------------------------\n'
    return ret
class CSDNSpider:
    def __init__(self,pageIdx=1,url="http://blog.csdn.net/fly_yr/article/list/1"):
        self.pageIdx = pageIdx
        self.url = url[0:url.rfind('/')+1]+str(pageIdx)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/60.0.3112.113 Safari/537.36',
            'Connection': 'keep - alive',
            'Upgrade - Insecure - Requests': '1',
            'Accept - Language': 'zh - CN, zh;q = 0.8',
            'Accept - Encoding': 'gzip, deflate',
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
            'Host': 'blog.csdn.net'
        }
    def getPages(self):
        req = urllib.request.Request(url=self.url,headers=self.headers)
        res = urllib.request.urlopen(req)

        data = res.read()
        data = ungzip(data)
        data = data.decode('utf-8')

        pages = r'<div.*?pagelist">.*?<span>.*?共(.*?)页</span>'
        pattern = re.compile(pages,re.DOTALL)
        pagesNum = re.findall(pattern,data)[0]
        return pagesNum

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
        for link1 in soup.find_all(attrs={"class":"list","id":"article_list"}):
            for link in link1.find_all(class_="list_item article_item"):
                try:
                    print(link)
                    print("###################################################")
                    ret.append(setData(link))

                except:
                    print("格式错误")
            print("_____________________________________________________")
        return ret
cs = CSDNSpider()
pagesNum = int(cs.getPages())
print("博文总数：",pagesNum)

for idx in range(pagesNum):
    cs.setPages(idx)
    print("当前页:",idx+1)

    papers = cs.readData()
    saveFile(papers,idx)
