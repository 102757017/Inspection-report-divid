from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import sys
import cv2
import numpy as np


WIDTH = 762
QUALITY = 300


def comp(obj):
    #cv2.IMREAD_COLOR表示以彩色模式读入图片
    
    img1 = cv2.imread('sample.png', cv2.IMREAD_COLOR)
    #由于opencv不支持读取中文路径，用以下方法代替cv2.imread
    img1 = cv2.imdecode(np.fromfile('sample.png', dtype=np.uint8), 1)
    
    img2 = cv2.imread(obj, cv2.IMREAD_COLOR)
    #由于opencv不支持读取中文路径，用以下方法代替cv2.imread
    img2 = cv2.imdecode(np.fromfile(obj, dtype=np.uint8), 1)
    
    #img2 =cv2.resize(img2,None,fx=0.7, fy=0.7, interpolation = cv2.INTER_CUBIC)


    
    #颜色转换函数，BGR->Gray 就可以设置为 cv2.COLOR_BGR2GRAY
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


    #SIFT
    sift= cv2.xfeatures2d.SIFT_create()
    #keypoints返回关键点
    keypoints1 = sift.detect(gray1, None)
    keypoints2 = sift.detect(gray2, None)


    #kp是关键点的列表，des是形状数组
    kp1,des1 = sift.compute(gray1,keypoints1)
    kp2,des2 = sift.compute(gray2,keypoints2)


    bf = cv2.BFMatcher()
    #返回k个最佳匹配  
    matches = bf.knnMatch(des1, des2, k=2)

    matchesMask = [[0,0] for i in range(len(matches))]


    #如果对一个列表，既要遍历索引又要遍历元素时可以使用enumerate()
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1,0]
    ppn=matchesMask.count([1,0])
    rato=ppn/len(matchesMask)
    return rato

os.chdir(os.path.dirname(__file__))



def title_page(uppages):
    title=[]
    titlepath=[]
    for index,x in enumerate(uppages):
        rato=comp(x)
        print(index,"特征点的匹配比率为",rato)
        if rato>0.2:
            title.append(index)
            titlepath.append(x)
    return title,titlepath



def splitpage(pages_path,titleindex):
    #每份成绩书末页页码
    end=[]
    for x in titleindex[1:]:
        end.append(x-1)
    end.append(len(pages_path)-1)

    #每份成绩书构成图片路径的list
    pdf=[]
    #所有成绩书pdf构成的list
    pdfs=[]
    for index,x in enumerate(pages_path):
        pdf.append(x)
        if index in end:
            pdfs.append(pdf)
            pdf=[]
    return pdfs


