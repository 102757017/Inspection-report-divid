 # -*- coding: UTF-8 -*-
from PIL import Image as Img
import os
import pprint
import sys
import shutil

sys.path.append(os.path.dirname(__file__))
from analysis_pic import detectTable
from ocr import tran_en,tran_ch
from judge import Judge_W,Judge_T
import shutil
import time
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter

import fitz
#from tkinter.filedialog import askopenfilename
from title import dis_title
import re


#清空output文件夹中所有的pdf
path=os.path.dirname(__file__)
output=os.path.join(path,"output")
list_dirs=os.walk(output)
for root, dirs, files in list_dirs:
    for f in files:
        # 分离文件名与扩展名，仅显示txt后缀的文件
        if os.path.splitext(f)[1]=='.pdf':
            file_path=os.path.join(root, f)
            os.remove(file_path)


#  打开PDF文件，生成一个对象
file_name="5.pdf"
doc = fitz.open(file_name)
#pdf页数
page_numbers=len(doc)

#%%
#封面的序列号构成的list
title_index=[]
part_nums=[]
for i in range(page_numbers):
    page = doc[i]
    # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
    zoom_x = 4
    zoom_y = 4
    trans = fitz.Matrix(zoom_x, zoom_y)
    pix = page.get_pixmap(matrix=trans, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    #莱文斯坦距离,两个字符串的编辑距离
    flag,text=dis_title(img)
    print("页面{},识别到的文本:{}，是否是封面:{}".format(i,text,flag))
    if flag==True:
        title_index.append(i)
        #输入PIL格式的图片，返回零件号大概区域的截图
        probably=detectTable(img)

        #ocr识别图片中的零件号
        result,img=tran_en(probably)
        img.save('./general_crop/page{}.jpg'.format(i))
        print(result)
        part_ts=result[0][1][0]
        part_wico=result[1][1][0]
 
        #去掉空格
        part_wico=re.sub(" ","",part_wico)
        part_ts=re.sub(" ","",part_ts)

        #去掉.
        part_wico=re.sub(r"\.","",part_wico)
        part_ts=re.sub(r"\.","",part_ts)
        
        #去掉/
        part_wico=re.sub("/","",part_wico)
        part_ts=re.sub("/","",part_ts)
        
        #将O替换为0
        part_ts=part_ts.replace("O","0")

        print("log:",part_wico)
        #去除WICO零件号中的括号，0,C、3也会被误判为括号
        part_wico=re.findall(r"[^【C0(（<:][0-9A-Z-]+[^3)）>】]", part_wico)[0]
        #查询数据库识别机种
        models=Judge_W(part_wico)

        #将TS零件号识别错误的页面筛选出来进行标记
        models2=Judge_T(part_ts)
        if models2==["unknow"]:
            models=["unknow"]

        #替换旧机种为新机种
        for i,m in enumerate(models):
            if m=="2LD":
                models[i]="3LQ"
            if m=="2QY":
                models[i]="3QY"
            if m=="2YC":
                models[i]="3YB"

                
        part_nums.append([part_ts,part_wico,models])
        print(part_ts,part_wico,models,"\n")


pdf = PdfReader(file_name)
#提取pdf的i~f页生成一个新的pdf
def gen_pdf(pdf,start,end):
    pdf_new = PdfWriter()
    for i in range(start,end):
        pdf_new.add_page(pdf.pages[i])
    return pdf_new

# %%
for i,j in enumerate(title_index):
    if i<len(title_index)-1:
        start=title_index[i]
        end=title_index[i+1]
    else:
        start=title_index[i]
        end=page_numbers
    part_pdf=gen_pdf(pdf,start,end)

    part_ts,part_wico,models=part_nums[i]
    for y in models:
        savepath=os.path.join(output,y,part_ts+".pdf")
        print("生成pdf文件:",savepath,part_wico)
        file=open(savepath,'wb')
        part_pdf.write(file)
        file.close()
