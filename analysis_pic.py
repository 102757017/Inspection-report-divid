# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np
from dbnet.dbnet_infer import DBNET,polygon_area
from utils import get_rotate_crop_image,pdf2img
import numpy as np
from PIL import Image

#输入PIL格式的图片，返回零件号大概区域的截图
def detectTable(image):
    #PIL to opencv
    img=cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)

    #图片先转成灰度的
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray",gray)


    #再把图片转换为二值图
    ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)  
    cv2.imshow("threshold",binary)


    #图片反色
    thresh_img = cv2.bitwise_not(binary)
    cv2.imshow("inverse",thresh_img)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()

    scale = 15
    #img.shape返回的是图像的行数，列数，色彩通道数.
    h_size = int(thresh_img.shape[1]/scale)

    '''
    构造形态学因子，形态学因子类似于笔刷，有不同的形状，并且有一个锚点
    此处构造了一个10*1的矩阵，形态学因子是矩形，锚点未定义时取中心值
    常用的形态学因子有如下几种：
    椭圆（MORPH_ELLIPSE）
    十字形结构（MORPH_CROSS）

    '''
    h_structure = cv2.getStructuringElement(cv2.MORPH_RECT,(10,1))


    #水平膨胀图像，相当于将笔刷沿轮廓外边缘绕行，返回笔刷锚点构成的封闭区
    img2 = thresh_img.copy()
    h_dilate_img = cv2.dilate(img2,h_structure,1)
    cv2.imshow("h_erode",h_dilate_img)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()

    v_structure = cv2.getStructuringElement(cv2.MORPH_RECT,(1,2))
    #垂直膨胀图像，相当于将笔刷沿轮廓外边缘绕行，返回笔刷锚点构成的封闭区
    v_dilate_img = cv2.dilate(h_dilate_img,v_structure,1)
    cv2.namedWindow("v_erode",0)
    cv2.imshow("v_erode",v_dilate_img)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()


    contours,hierarchy= cv2.findContours(v_dilate_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
    print("轮廓数量:",len(contours))#共几个轮廓


    '''第一个参数是指明在哪幅图像上绘制轮廓；
    第二个参数是轮廓本身，在Python中是一个list。
    第三个参数指定绘制轮廓list中的哪条轮廓，如果是-1，则绘制其中的所有轮廓。
    第四个参数表示颜色
    第五个参数表示轮廓线的宽度，如果是-1，则为填充模式'''
    img3 = img.copy()
    cv2.drawContours(img3,contours,-1,(0,0,255),2)


    #cv2.contourArea计算轮廓面积,返回轮廓内像素点的个数，此处将轮廓集按面积排序
    c = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    #cv2.minAreaRect主要求得包含点集最小面积的矩形，这个矩形是可以有偏转角度的，可以与图像的边界不平行。
    rect = cv2.minAreaRect(c)
    print("生成最小矩形:",rect)
    box = np.int0(cv2.boxPoints(rect))
    cv2.drawContours(img3, [box], -1, (0, 255, 0), 3)
    cv2.imshow("largest shape",img3)
    #cv2.waitKey(0)  
    cv2.destroyAllWindows()

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    x3=int(x1+width*0.72)
    y3=int(y1+hight*0.02)
    x4=x2
    y4=int(y2-hight*0.91)
    #cropImg = img[y1:y2, x1:x2]
    cropImg = img[y3:y4, x3:x4]

    #gray2 = cv2.cvtColor(cropImg,cv2.COLOR_BGR2GRAY)
    #ret2, binary2 = cv2.threshold(gray2,127,255,cv2.THRESH_BINARY)  
    cv2.imshow("threshold",cropImg)
    cv2.imwrite('bbb.jpg',cropImg)

    #cv2.waitKey(0)  
    cv2.destroyAllWindows()
    return cropImg


#输入零件号大概区域的截图，返回零件号精确区域的PIL格式截图 
def extract_part(img):
    text_handle = DBNET(MODEL_PATH="./models/dbnet.onnx")
    box_list, score_list = text_handle.process(img,short_size=32*6)
    #print("置信度",score_list)
    #img2 = draw_bbox(img, box_list)
    #cv2.imwrite("test.jpg", img2)

    area=polygon_area(box_list)
    index=area.index(max(area))

    #将截图边框扩大一点
    b=box_list[index]
    b[0][0]=b[0][0]-5
    b[3][0]=b[0][0]
    b[1][0]=b[1][0]+5
    b[2][0]=b[1][0]
    b[0][1]=b[0][1]-5
    b[1][1]=b[0][1]
    b[2][1]=b[2][1]+5
    b[3][1]=b[2][1]

    crop_img = get_rotate_crop_image(img, b.astype(np.float32))
    print(box_list[index])
    
    #图片先转成灰度的
    gray = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)

    #再把图片转换为二值图
    ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY) 
    
    #膨胀图像
    structure = cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2))
    binary = cv2.erode(binary,structure,1)

    cv2.imshow("threshold",binary)
    #cv2.waitKey(0)
    binary=Image.fromarray(cv2.cvtColor(binary,cv2.COLOR_BGR2RGB))

    return binary

if __name__=="__main__":
    #提取pdf的页面转换为PIL格式的图片
    img=pdf2img("a.pdf",12)
    #输入PIL格式的图片，返回零件号大概区域的截图
    b=detectTable(img)
    extract_part(b)