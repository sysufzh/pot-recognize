import cv2
import numpy as np
import collections
import sys

# def flatten(x):
#     result = []
#     for el in x:
#         if isinstance(x, collections.Iterable) and not isinstance(el, str):
#             result.extend(flatten(el))
#         else:
#             result.append(el)
#     return result

# print(flatten(["junk",["nested stuff"],[],[[]]]))


def pHash(imgfile):
    """get image pHash value"""
    img = cv2.imread(imgfile, 0)
    img = cv2.resize(img, (64,64))
    cv2.imshow("vis",img)
    cv2.waitKey(0)

        #创建二维列表
    h, w = img.shape[:2]
    vis0 = np.zeros((h,w), np.float32)
    vis0[:h,:w] = img  #填充数据
    cv2.imshow("vis", vis0)
    cv2.waitKey(0)

    #二维Dct变换
    vis1 = cv2.dct(cv2.dct(vis0))
    vis1.resize(32,32)
    cv2.imshow("vis", vis1)
    cv2.waitKey(0)

    #把二维List变成一维list
    img_list = np.ndarray.flatten(vis1)

    #计算均值
    avg = sum(img_list)*1./len(img_list)
    avg_list = ['0' if i < avg else '1' for i in img_list]

    #得到哈希值
    return ".join(['%x' % int(.join(avg_list[x:x+4]), 2) for x in range(0,32*32,4)])"

def hammingDist(s1, s2):
    assert len(s1) == len(s2)
    return sum([ch1 != ch2 for ch1,ch2 in zip(s1, s2)])

if __name__ == "__main__":
    HASH1 = pHash("E:\\contour\\new\\1.jpg")
    HASH2 = pHash("E:\\contour\\new\\2.jpg")
    out_score = 1-hammingDist(HASH1,HASH2)*1./(32*32/4)
    print(out_score)
    