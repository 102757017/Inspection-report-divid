from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import sys
import cv2
import numpy as np
from dbnet.dbnet_infer import DBNET,polygon_area
from utils import get_rotate_crop_image
from ocr import tran_text
from PIL import Image
import Levenshtein
import fitz
import numpy as np
from utils import pdf2img

WIDTH = 762
QUALITY = 300


def dis_title(img):
    img = img.crop((700, 420, 1550, 700))
    #PIL to opencv
    img=cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
    
    text_handle = DBNET(MODEL_PATH="./models/dbnet.onnx")
    box_list, score_list = text_handle.process(img,short_size=32*6)
    #print("置信度",score_list)
    #img2 = draw_bbox(img, box_list)
    #cv2.imwrite("test.jpg", img2)

    #矩形的面积
    area=polygon_area(box_list)
    if len(area)>0:
        #最大的矩形的索引
        index=area.index(max(area))
        crop_img = get_rotate_crop_image(img, box_list[index].astype(np.float32))
        crop_img=Image.fromarray(cv2.cvtColor(crop_img,cv2.COLOR_BGR2RGB))
        text=tran_text(crop_img)
        #print("识别到的文本",text)
        #莱文斯坦距离,两个字符串的编辑距离
        distance=Levenshtein.distance(text,"武汉提爱思全兴汽车零都件有限公司")

    else:
        distance=Levenshtein.distance("","武汉提爱思全兴汽车零都件有限公司")

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
    img=pdf2img("a.pdf",0)

    flag,text=dis_title(img)
    print("是否是封面",flag)
