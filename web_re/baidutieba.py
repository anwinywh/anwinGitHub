# coding=utf-8

'''
    爬取百度贴吧帖子
    Created by  anwin on 2017/11/22.
'''

import re
import urllib2

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    #sub(pattern, repl, string, count=0, flags=0)
    #对字符串string按照正则表达式pattern，将string的匹配项替换成字符串repl
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

#百度贴吧爬虫类
class BDTB:

    # 初始化，传入基地址，是否只看楼主的参数
    def __init__(self, baseUrl, seeLZ, floorTag):
        # base链接地址
        self.baseURL = baseUrl
        # 是否只看楼主
        self.seeLZ = '?see_lz=' + str(seeLZ)
        # HTML标签剔除工具类对象
        self.tool = Tool()
        # 全局file变量，文件写入操作对象
        self.file = None
        # 楼层标号，初始为1
        self.floor = 1
        # 默认的标题，如果没有成功获取到标题的话则会用这个标题
        self.defaultTitle = u"百度贴吧"
        # 是否写入楼分隔符的标记
        self.floorTag = floorTag

    # 传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            # 构建URL
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            print "最终网页链接地址为 ：" + url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # 返回UTF-8格式编码内容
            return response.read().decode('utf-8')
        # 无法连接，报错
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接百度贴吧失败,错误原因", e.reason
                return None

    # 获取帖子一共有多少页
    def getPageNum(self, page):
        # 获取帖子页数的正则表达式
        pattern = re.compile('<span class="red">(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    # 获取帖子标题
    def getTitle(self, page):
        pattern = re.compile('style="width: 416px">(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    #设置标题
    def setFileTitle(self, title):
        # 如果标题不是为None，即成功获取到标题
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaultTitle + ".txt", "w+")

    # 获取每一层楼的内容,传入页面内容
    def getContent(self, page):
        # 匹配所有楼层的内容
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            # 将文本进行去除标签处理，同时在前后加入换行符
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content.encode('utf-8'))
        return contents

    #写入数据
    def writeData(self, contents):
        #向文件写入每一楼的信息
        for item in contents:
            if self.floorTag == '1':
                # 楼之间的分隔符
                floorLine = "\n" + str(self.floor) + u"------------------\n"
                self.file.write(floorLine)

            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print u"URL已经失效，请重新获取"
            return
        try:
            print "该帖子共有 " + str(pageNum) + " 页"
            #range() 函数可创建一个整数列表，一般用在 for 循环中
            #start: 计数从 start 开始。默认是从 0 开始。例如range（5）等价于range（0， 5）;
            #end: 计数到 end 结束，但不包括 end。例如：range（0， 5） 是[0, 1, 2, 3, 4]没有5
            #step：步长，默认为1。例如：range（0， 5） 等价于 range(0, 5, 1)
            for i in range(1, int(pageNum)+1):
                print "正在写入第" + str(i) + "页数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        # 出现写入异常
        except IOError, e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成"

# print u"请输入帖子代号"
# baseURL = 'https://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
baseURL = raw_input("请输入帖子链接\n")
baseURL = baseURL.strip()  #防止用户多输入了空格键
seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
print "baseURL="+baseURL + " seeLZ="+seeLZ + " floorTag="+floorTag;

adtb = BDTB(baseURL, seeLZ, floorTag)
adtb.start()