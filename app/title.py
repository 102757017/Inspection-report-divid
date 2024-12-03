from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import sys
import cv2
import numpy as np
from ocr import tran_ch
from PIL import Image
import Levenshtein
import fitz
import numpy as np
from utils import pdf2img


#输入PIL格式的图片，返回零件号大概区域的截图
def detectTable(image):
    #PIL to opencv
    img=cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)

    #图片先转成灰度的
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


    #再把图片转换为二值图
    ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)  


    #图片反色
    thresh_img = cv2.bitwise_not(binary)


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
    


    v_structure = cv2.getStructuringElement(cv2.MORPH_RECT,(1,2))
    #垂直膨胀图像，相当于将笔刷沿轮廓外边缘绕行，返回笔刷锚点构成的封闭区
    v_dilate_img = cv2.dilate(h_dilate_img,v_structure,1)
    #cv2.imshow("v_dilate_img",v_dilate_img)
    

    contours,hierarchy= cv2.findContours(v_dilate_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
    #print("轮廓数量:",len(contours))#共几个轮廓


    '''第一个参数是指明在哪幅图像上绘制轮廓；
    第二个参数是轮廓本身，在Python中是一个list。
    第三个参数指定绘制轮廓list中的哪条轮廓，如果是-1，则绘制其中的所有轮廓。
    第四个参数表示颜色
    第五个参数表示轮廓线的宽度，如果是-1，则为填充模式'''
    img3 = img.copy()
    cv2.drawContours(img3,contours,-1,(0,0,255),2)
    
    


    #cv2.contourArea计算轮廓面积,返回轮廓内像素点的个数，此处将轮廓集按面积排序,找出面积最大的轮廓
    c = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    #cv2.minAreaRect找到一个包围指定轮廓的最小面积矩形，这个矩形是可以有偏转角度的，可以与图像的边界不平行。
    rect = cv2.minAreaRect(c)
    #print("生成最小矩形:",rect)
    box = np.int0(cv2.boxPoints(rect))
    cv2.drawContours(img3, [box], -1, (0, 255, 0), 3)
    #cv2.imshow("img3",img3)
    #cv2.imwrite('bbb.jpg',img3)


    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    x3=int(x1+width*0.25)
    y3=int(y1+hight*0.03)
    x4=int(x1+width*0.63)
    y4=int(y1+hight*0.08)
    #cropImg = img[y1:y2, x1:x2]
    cropImg = img[y3:y4, x3:x4]


    #gray2 = cv2.cvtColor(cropImg,cv2.COLOR_BGR2GRAY)
    #ret2, binary2 = cv2.threshold(gray2,127,255,cv2.THRESH_BINARY)  
    #cv2.imshow("threshold",cropImg)
    #cv2.imwrite('bbb.jpg',cropImg)

    cv2.waitKey(0)  
    cv2.destroyAllWindows()
    return cropImg



def dis_title(img):
    #截取公司名称的图片
    img=detectTable(img)
    #PIL to opencv
    img=cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
    #cv2.imshow("img",img)
    #cv2.imwrite("tsname.jpg",img)
    result,img=tran_ch(img)
    #print(result)
    
    
    if len(result)>0:
        text=result[0][1][0]
        #print("识别到的文本",text)
        #莱文斯坦距离,两个字符串的编辑距离
        distance=Levenshtein.distance(text,"武汉提爱思全兴汽车零都件有限公司")

    else:
        distance=Levenshtein.distance("","武汉提爱思全兴汽车零都件有限公司")
        text=""

    if  distance<5:
        #print(index,distance,"此页是封面")
        flag=True
    else:
        #print(index,distance)
        flag=False
    return flag,text


os.chdir(os.path.dirname(__file__))



def title_page(uppages):
    title=[]
    titlepath=[]
    for index,x in enumerate(uppages):
        distance=dis_title(x)
        if  distance<5:
            print(index,distance,"此页是封面")
            title.append(index)
            titlepath.append(x)
        else:
            print(index,distance)
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



if __name__=="__main__":
    #提取pdf的页面转换为PIL格式的图片
    img=pdf2img("4.pdf",49)

    flag,text=dis_title(img)
    print("识别到的文本",text)
    print("是否是封面",flag)
