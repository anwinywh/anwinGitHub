# coding=utf-8

'''
app Icon图标生成工具，图标大小可修改数组imageSize里面的大小
by anwin  2018-05-07
'''

from PIL import  Image

imageSize = [76,120,152,167,180,1024]


def createImage(iconPash, size):
    im = Image.open(iconPash)
    im.resize((size, size), Image.ANTIALIAS).save(iconPash + "icon%dx%d.png" % (size, size))

# 开始剪辑图片
def start():
    iconPathStr = raw_input("请输入图片路径，具体到图片名:")

    for size in imageSize:
        createImage(iconPathStr,size)


start()


