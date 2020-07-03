# -*- coding:utf-8 -*-

import os
import time
import shutil

from PIL import Image
from psd_tools import PSDImage
import cv2


from math import floor, ceil
import numpy as np

import re


def StripExt(filename):
    name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1] 
    #把filename分成列表，第一个元素为文件名，第二个元素为后缀名
    return name,ext

def TransChinese(img_path, SiteName):
#将要处理的中文括号，冒号改为英文括号，横杠

    for root, dirs, files in os.walk(img_path):
        for a in files:
            if (a.endswith('.psd') == True):
                b = a
                if '（' in a:
                    a = a.replace('（','(')
                if '）' in a:
                    a = a.replace('）',')')
                if '：' in a:
                    a = a.replace('：','-')
                if ':' in a:
                    a = a.replace(':','-')
                b, a = os.path.join(root,b), os.path.join(root,SiteName + a)
                try:
                    os.renames(b, a)
                except FileExistsError:
                    a = os.path.splitext(a)[0] +'(1)' + os.path.splitext(a)[1]
                    os.rename(b, a)
                d = a.replace('psd','png')
                psd = PSDImage.open(a)
                image = psd.compose()
                image.save(d)
                # print('正在操作'+ b +'到'+ a)
    print('psd2png转换完成')

def del_files(img_path):

# 删除文件夹中非png后缀的文件，只留下png后缀的文件

    for root, dirs, files in os.walk(img_path):
        for name in files:
            if (name.endswith('.png') == False):
                os.remove(os.path.join(root, name))

def read_rgb_img(filename):

# cv2读取图片，彩色模式
# filename: 文件路径，到文件名

    rgb_img = cv2.imread(filename, cv2.IMREAD_COLOR)
    return rgb_img

def convert_rgb2gray(img):

# cv2转换模式，从彩色到灰度
#   img: cv2读取的图片

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.GaussianBlur(gray_img, (5,5), 0)
    # 采用高斯滤波去掉噪点
    return gray_img

def convert_gray2binary(img):

# 二值化处理
# img: cv2灰度图片

    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize= (3, 3))
    cl1 = clahe.apply(img)
    # CLAHE 自适应直方图均衡化

    edge = cv2.Canny(cl1,100,200)
    # binary_img = cv2.adaptiveThreshold(edge, 
    #                                     255, 
    #                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    #                                     cv2.THRESH_BINARY_INV, 3, 2)
    #                                     #这两个参数是blocksize的大小，数字越小，轮廓越精准，但也越不平滑
    _, binary_img = cv2.threshold(edge,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return binary_img

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return contours

def draw_contours(contour_path, filename, img, contours):
    # ArcLength = []
    ContourArea = []
    for i in range(len(contours)):
        ContourArea.append(cv2.contourArea(contours[i]))
    index = ContourArea.index(max(ContourArea)) #只画面积最大的轮廓，有时算面积比算周长更好
    thickness = 2
    # thickness of contours
    color = (0,0,0)
    temp = np.ones(img.shape, np.uint8)*255
    cv2.drawContours(temp, contours, index, color, thickness)
    cv2.imwrite(contour_path + '\\' + filename + '(CT)' + '.jpg', temp)

def png2contour(img_path, contour_path):
    for root, dirs, files in os.walk(img_path):
        for name in files:
            png_name = os.path.join(root, name)
            filename, ext = StripExt(name)
            rgb_img = read_rgb_img(png_name)
            gray_img = convert_rgb2gray(rgb_img)
            binary_img = convert_gray2binary(gray_img)
            contours = getContours(binary_img)
            draw_contours(contour_path, filename, binary_img, contours)

def MoveFile(img_path, move_path):
    for root, dirs, files in os.walk(img_path):
        for name in files:
            png_name = os.path.join(root,name)
            shutil.move(png_name, move_path)

if __name__ == "__main__":
    img_path = 'E:\\Change'
    contour_path = 'E:\\contour\\try'
    move_path = 'E:\\allpng'
    SiteName = input('Please enter the sitename:')
    TransChinese(img_path, SiteName)
    time.sleep(1)
    del_files(img_path)
    time.sleep(2)
    png2contour(img_path, contour_path)
    MoveFile(img_path, move_path)
    print('Finish!')
    
