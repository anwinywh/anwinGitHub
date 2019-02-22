# -*- coding: utf-8 -*-

'''
图片集切割工具
支持json，大图格式为png, jpg格式的图片集
把图片集放到rootdir下，json文件和大图一起放
不同的工具导出的json文件不一样 具体操作看json_to_dict里相关的key
by anwin 2019-02-22
'''

import os, sys
import json
import os
import os.path
from PIL import Image


#解析json文件，不同的结构具体解析
def json_to_dict(json_filename):
    json_file = open(json_filename, 'r')
    all_pic_dic = json.load(json_file)
    all_item_list = []
    for one_pic_item in all_pic_dic['frames']:
        one_json_item = all_pic_dic['frames'][one_pic_item]
        one_item = {}
        one_item['name'] = one_pic_item.replace('_png', '') #可能带扩展名保存，去除一下  strip： 用来去除头尾字符、空白符(包括\n、\r、\t、' '，即：换行、回车、制表符、空格) lstrip：用来去除开头字符、空白符(包括\n、\r、\t、' '，即：换行、回车、制表符、空格) rstrip：用来去除结尾字符、空白符(包括\n、\r、\t、' '，即：换行、回车、制表符、空格) 注意：这些函数都只会删除头和尾的字符，中间的不会删除。
        one_item['x'] = one_json_item['x']
        one_item['y'] = one_json_item['y']
        one_item['w'] = one_json_item['w']
        one_item['h'] = one_json_item['h']
        all_item_list.append(one_item)

    return all_item_list


def gen_png_from_json(folder_name, json_filename, png_filename):
    big_image = Image.open(png_filename)
    all_item_list = json_to_dict(json_filename)

    print 'gen_png_from_json:' + folder_name

    # 清理掉原目录
    if not os.path.isdir(folder_name):
        # os.removedirs(folder_name)
        os.mkdir(folder_name)

    for i, one_item_data in enumerate(all_item_list):
        file_name = one_item_data['name']
        x = one_item_data['x']
        y = one_item_data['y']
        w = one_item_data['w']
        h = one_item_data['h']

        # 设置图像裁剪区域 (x左上，y左上，x右下,y右下)
        image_box = [x, y, x + w, y + h]
        one_pic = big_image.crop(image_box)

        one_pic.save(folder_name + "/" + file_name + '.png')  # 存储裁剪得到的图像

        # print one_item_data


def packdirHandle(rootdir):
    file_name_set = set()
    if os.path.exists(rootdir):
        list_file = os.listdir(rootdir)
        for i in range(0, len(list_file)):
            one_file_name = list_file[i]
            path = os.path.join(rootdir, one_file_name)
            if os.path.isfile(path):
                file_name_set.add(os.path.splitext(one_file_name)[0])

    for file_name in file_name_set:
        json_filename = os.path.join(rootdir, file_name) + '.json'
        png_filename = os.path.join(rootdir, file_name) + '.png'
        jpg_filename = os.path.join(rootdir, file_name) + '.jpg'

        if os.path.exists(json_filename):
            if os.path.exists(png_filename):
                try:
                    gen_png_from_json(os.path.join(rootdir, file_name), json_filename, png_filename)
                except Exception:
                    print '!!!!!!!!!!!!!!!!!!!!' + json_filename + ' json error !!!!!!!!!!!!!!!!!!!!!'
            elif os.path.exists(jpg_filename):
                try:
                    gen_png_from_json(os.path.join(rootdir, file_name), json_filename, jpg_filename)
                except Exception:
                    print '!!!!!!!!!!!!!!!!!!!!' + json_filename + ' json error !!!!!!!!!!!!!!!!!!!!!'


if __name__ == '__main__':

    # rootdir = sys.argv[1]  #用终端执行py文件的时候用到的路径 当前py文件的路径
    # rootdir = "/Users/anwin/Desktop/test/effect"
    rootdir = raw_input("请输入图片集目录:")
    packdirHandle(rootdir)



