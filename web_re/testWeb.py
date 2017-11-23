#encoding:utf-8

import urllib
import re   #导入正则表达式

# ****************** 获取网页资源 ****************** #
def getHtml(url):
    page = urllib.urlopen(url)  #打开网页并下载
    html = page.read()
    return html

html = getHtml("http://192.168.16.176:5368/index.html")
# print html
# ****************** 获取网页资源 ****************** #

# ****************** 获取网页图片资源 ****************** #
def getImg(html):
    reg = r'src="(.+?\.jpg)" pic_ext'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    x = 0
    for imgurl in imglist:
        urllib.urlretrieve(imgurl, '%s.jpg' % x)
        x += 1

print getImg(html)
# ****************** 获取网页图片资源 ****************** #

