#encoding:utf-8
# 文件名：regexTest.py
# 练习使用正则表达式
# by anwin  2017-11-07

import os
import sys
import re


PackageName = "com.yaowan.dfh3.uc"

path = os.path.split(os.path.realpath(sys.argv[0]))[0]  #得到文件所在路径
path = os.path.dirname(path)   #得到上一层目录
# print(path)

dataPath = path + "/data/AndroidManifest.xml"   #得到指定文件
dstPath = dataPath
# print(dstPath)

def changePackageName():
    rf = open(dataPath, 'r') #'r'读模式、'w'写模式、'a'追加模式、'b'二进制模式、'+'读/写模式
    line = rf.readline()   # 1、read( )：表示读取全部内容 2、readline( )：表示逐行读取
    allText = ""

    while line:
        text = parse(line)
        allText += text
        line = rf.readline()    #为了循环重新改变line的值进行循环
    rf.close()

    writeFile = open(dstPath, 'w')
    writeFile.write(allText)
    writeFile.close()
    print "------修改包名成功------"

def parse(text):
    matchObj = re.search('(.*?package=")(com.*?)("[\s\S]*)', text)
    if matchObj:
        #group是针对（）来说的，group（0）就是指的整个串，group（1） 指的是第一个括号里的东西，group（2）指的第二个括号里的东西
        #正则表达式的括号
        text = matchObj.group(1) + PackageName + matchObj.group(3)

    matchObj = re.search('(.*?android:name=")(com.tencent.*?)(\.intent.action.COMMAND"[\s\S]*)', text)
    if matchObj:
        text = matchObj.group(1) + PackageName + matchObj.group(3)

    matchObj = re.search('(.*?android:name=")(com.yaowan.*?)(\.intent.action.COMMAND"[\s\S]*)', text)
    if matchObj:
        text = matchObj.group(1) + PackageName + matchObj.group(3)

    matchObj = re.search('(.*?android:authorities=")(com.*?)(\.umeng.message"[\s\S]*)', text)
    if matchObj:
        text = matchObj.group(1) + PackageName + matchObj.group(3)

    matchObj = re.search('(.*?android:authorities=")(com.*?)(\.unicorn.fileprovider"[\s\S]*)', text)
    if matchObj:
        text = matchObj.group(1) + PackageName + matchObj.group(3)

    return text


changePackageName()