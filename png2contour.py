import cv2

import os
import time
import shutil

from math import floor, ceil
import numpy as np



def StripExt(filename):
    name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1] 
    #把filename分成列表，第一个元素为文件名，第二个元素为后缀名
    return name,ext

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
    # cv2.imshow("img",img)
    # cv2.waitKey(0)
    # EqualizeImg = cv2.equalizeHist(img)
    # 全局直方图均衡化

    clahe = cv2.createCLAHE(clipLimit=1, tileGridSize= (3,3))
    # clipLimit的参数在1-80之间调整
    EqualizeImg = clahe.apply(img)
    # # 自适应直方图均衡化
    # cv2.imshow("img",EqualizeImg)
    # cv2.waitKey(0)

    edge = cv2.Canny(EqualizeImg,100,200) 
    # canny算子的两个参数：minval,maxval,低于minval的直接舍弃，高于maxval的直接认为是真正的边缘，二者之间则判断是否与真正的边界相连
    # cv2.imshow("img",edge)
    # cv2.waitKey(0)
    # binary_img = cv2.adaptiveThreshold(edge, 
    #                                     255, 
    #                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    #                                     cv2.THRESH_BINARY_INV, 3, 2)  
                                        #这两个参数是blocksize的大小，数字越小，轮廓越精准，但也越不平滑
    # _, binary_img = cv2.threshold(edge,190,255,cv2.THRESH_BINARY)
    #非自适应阈值
    _, binary_img = cv2.threshold(edge,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # cv2.imshow("img",binary_img)
    # cv2.waitKey(0)
    return binary_img

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return contours

def draw_contours(contour_path, filename, img, contours):
    # ArcLength = []
    # for i in range(len(contours)):
    #     ArcLength.append(cv2.arcLength(contours[i], True)) 
    # index = ArcLength.index(max(ArcLength))
    # #只画周长最大的轮廓
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

if __name__ == "__main__":
    img_path = 'E:\\Change'
    contour_path = 'E:\\contour\\try'
    png2contour(img_path, contour_path)
    print('Finish!')