import urllib.request,gzip,re,http.cookiejar,urllib.parse
import sys

def ungzip(data):
    try:
        print("正在解压...")
        data = gzip.decompress(data)
        print("解压完毕...")
    except:
        print("未压缩...")
    return data

def getOpener(header):
    cookieJar = http.cookiejar.CookieJar()
    cp = urllib.request.HTTPCookieProcessor(cookieJar)
    opener = urllib.request.build_opener(cp)
    headers = []
    for key,value in header.items():
        elem = (key,value)
        headers.append(elem)
    opener.addheaders = headers
    return opener

def getXsrf(data):
    cer = re.compile('name=\"_xsrf\" value=\"(.*)\"',flags=0)
    strlist = cer.findall(data)
    return  strlist[0]

headers = {
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate,br',
    'Host': 'www.zhihu.com',
    'DNT':'1',
    'Cache-Control':'max-age=0',
    'Upgrade-Insecure-Requests':'1',
    'Referer':'https://www.zhihu.com/'
}

url = "https://www.zhihu.com/"
req = urllib.request.Request(url,headers=headers)
res=urllib.request.urlopen(req)

data = res.read()
data = ungzip(data)
print(data)
_xsrf = getXsrf(data.decode('utf-8'))
print(_xsrf)
opener = getOpener(headers)
url += '#signin'
account='18840829170'
passwd='yanfeilong123'
postDict={
    '_xsrf':_xsrf,
    'account':account,
    'password':passwd,
    'remember_me':'true'
}
postData=urllib.parse.urlencode(postDict).encode()

#构造请求
res=opener.open(url,postData)
data = res.read()
#解压缩
data = ungzip(data)
print(data.decode())