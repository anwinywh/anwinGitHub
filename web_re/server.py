#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：client.py

import socket    # 导入 socket 模块

s = socket.socket()  # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port = 12345   #设置好端口号
s.bind(host, port)  #绑定端口

s.listen(5)   #等待客户端链接

while True:
    c, addr = s.accept()   #建立客户端链接
    print  '链接地址 : '+addr
    c.send('已连接成功，欢迎您!')
    c.close();    #关闭连接