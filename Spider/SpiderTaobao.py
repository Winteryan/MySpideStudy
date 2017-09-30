import urllib.request,socket,re,sys,os,gzip
from bs4 import  BeautifulSoup
import json
import requests
targetPath = "F:\\Spider\\MM"
#H5主页数据URL1
#https://acs.m.taobao.com/h5/mtop.taobao.daren.accountpage.componentization.render/1.0/?jsv=2.4.3
#&appKey=12574478&t=1506758236688&sign=eef40d8c73bb88a3fa301bc15d2c182f&api=mtop.taobao.daren.accountpage.componentization.render&v=1.0
#&data=%7B%22darenId%22%3A%22703596186%22%2C%22components%22%3A%22loft%2Cappbar%2CheaderKol%2Ctools%2CmainData%2Ctab%2Crecommend%2CgroupChat%2Cliving%2Cfeeds%2CfooterMenu%22%7D
#H5主页数据URL2
#https://acs.m.taobao.com/h5/mtop.taobao.daren.accountpage.feeds/1.0/?jsv=2.4.3&appKey=12574478&t=1506758237447
#&sign=ed1697b9223a9b5bfb3db3a776f81cd9&api=mtop.taobao.daren.accountpage.feeds&v=1.0&AntiCreep=true
# &data=%7B%22currentPage%22%3A1%2C%22force%22%3A2%2C%22accountId%22%3A%22703596186%22%7D
def ungzip(data):
    try:
        data = gzip.decompress(data)
    except:
        print("未经压缩，无需解压...")
    return data
def saveImg(Imgpath,data):
    FilePath = "F:\\Spider\\TBMM\\"+data["darenNick"]
    if not os.path.isdir(FilePath):
        os.makedirs(FilePath)
    pos = Imgpath.rindex('/')
    t = os.path.join(FilePath, Imgpath[pos + 1:] + ".jpg")
    return t

def saveFile(data,Videodata,Productiondata):
    path = "F:\\Spider\\TBMM\\"+data["darenNick"]+"\\Information.txt"
    file = open(path, 'w')
    try:
        file.write("============================基本信息===============================" + "\n")
        file.write("用户ID:"+str(data["userId"])+"\n")
        file.write("用户昵称:" + str(data["darenNick"]) + "\n")
        file.write("简介：" + str(data["desc"]) + "\n")
        if str(data["profileUrlH5"]).startswith("http"):
            file.write("个人主页：" + str(data["profileUrlH5"]) + "\n")
        else:
            data["profileUrlH5"]="https:"+str(data["profileUrlH5"])
            file.write("个人主页：" + data["profileUrlH5"] + "\n")
        if str(data["profileUrlPc"]).startswith("http"):
            file.write("个人淘宝主页：" + str(data["profileUrlPc"]) + "\n")
        else:
            data["profileUrlPc"]="https:"+str(data["profileUrlPc"])
            file.write("个人淘宝主页：" + data["profileUrlPc"] + "\n")
        file.write("=============================END=================================="+"\n\n\n")
        file.write("===========================直播信息===============================" + "\n")
        for i in range(len(Videodata)):
            for k in range(len(Videodata[i])):
                vdata = Videodata[i][k]
                file.write("直播标题:" + str(vdata["title"]) + "\n")
                file.write("时间:" + str(vdata["startTime"]) + "\n")
                file.write("观看人数:" + str(vdata["totalJoinCount"]) + "\n")
                if str(vdata["url"]).startswith("http"):
                    file.write("直播地址:" + str(vdata["url"]) + "\n")
                else:
                    vdata["url"] = "https:" + str(vdata["url"])
                    file.write("直播地址:" + str(vdata["url"]) + "\n")
                file.write("*****************************************************************" + "\n")
        file.write("==============================END=================================" + "\n\n\n")
        file.write("===========================产品信息===============================" + "\n")
        for i in range(len(Productiondata)):
            for k in range(len(Productiondata[i])):
                pdata = Productiondata[i][k]
                file.write("产品标题:" + str(pdata["title"]) + "\n")
                file.write("产品介绍:" + str(pdata["summary"]) + "\n")
                file.write("阅读人数:" + str(pdata["readNum"]) + "\n")
                if str(pdata["url"]).startswith("http"):
                    file.write("链接:" + str(pdata["url"]) + "\n")
                else:
                    pdata["url"] = "https:" + str(pdata["url"])
                    file.write("链接:" + str(pdata["url"]) + "\n")
                file.write("*****************************************************************" + "\n")
        file.write("==============================END=================================" + "\n\n\n")
    except:
        file.close()
        return
    file.close()

class MMSpider:
    def __init__(self,pageIdx=1,url="https://mm.taobao.com/alive/list.do?scene=all&page=1"):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/60.0.3112.113 Safari/537.36',
            'Accept': '* / *',
            'Accept - Encoding':'gzip, deflate, br',
            'Accept - Language': 'zh - CN, zh;q = 0.8',
            'Connection': 'keep - alive'
        }
        self.data = {
            'callback': 'jsonp113',
            'tce_sid': '1407246',
            'tce_vid': '2',
            'tid':'',
            'tab':'',
            'topic':'',
            'count':'',
            'env': 'online',
            'scene': 'all'

        }
        self.url = url[0:url.rfind('=')+1]+str(pageIdx)

    def readData(self):
        req = urllib.request.Request(url=self.url, headers=self.headers)
        res = urllib.request.urlopen(req)
        data = res.read()
        data = ungzip(data)
        data = data.decode('gbk')
        data = json.loads(data,"gbk")
        return data

    def getUrl(self,idx):
        self.url = self.url[0:self.url.rfind('=')+1]+str(idx)

    def setUrl(self,url):
        self.url = url

    def getPages(self):
        req = urllib.request.Request(url=self.url, headers=self.headers)
        res = urllib.request.urlopen(req)
        data = res.read()
        data = ungzip(data)
        data = data.decode('gbk')
        data = json.loads(data, "gbk")
        return data["totalPage"]

MM = MMSpider()
total = int(MM.getPages())
for i in range(total):
    MM.getUrl(i+1)
    DATA = MM.readData()["dataList"]
    for data in DATA:
        # print(data["avatarUrl"])
        Imgdata = []
        Videodata = []
        Productiondata = []
        MM2 = MMSpider()
        MM2.setUrl("https://v.taobao.com/micromission/daren/get_productions.do?userId=" + str(data["userId"]))
        # print(MM2.readData()["data"]["liveVideos"])
        try:
            DATA2 = MM2.readData()["data"]
        except:
            continue
        if "liveVideos" in str(str(DATA2)):
            Videodata.append(DATA2["liveVideos"])
            for data2 in DATA2["liveVideos"]:
                try:
                    if str(data2["coverImg"]).startswith("http"):
                        Imgdata.append(data2["coverImg"])
                    else:
                        data2["coverImg"] = "https:" + data2["coverImg"]
                        Imgdata.append(data2["coverImg"])
                except:
                    continue
        if "production" in str(str(DATA2)):
            Productiondata.append(DATA2["production"])
            for data3 in DATA2["production"]:
                try:
                    if str(data3["pic"]).startswith("http"):
                        Imgdata.append(data3["pic"])
                    else:
                        data3["pic"] = "https:" + data3["pic"]
                        Imgdata.append(data3["pic"])
                except:
                    continue
        try:
            if str(data["avatarUrl"]).startswith("http"):
                Imgdata.append(data["avatarUrl"])
            else:
                data["avatarUrl"] = "https:"+data["avatarUrl"]
                Imgdata.append(data["avatarUrl"])
        except:
            continue
        for imgurl in Imgdata:
            try:
                urllib.request.urlretrieve(imgurl, saveImg(imgurl,data))
            except:
                continue
        saveFile(data,Videodata,Productiondata)


