 # -*- coding: UTF-8 -*-
from PIL import Image as Img
import os
import pprint
import sys
import shutil

sys.path.append(os.path.dirname(__file__))
from analysis_pic import detectTable,extract_part
from ocr import tran_text
from judge import Judge
import shutil
import time
from chardeel import Rnoise
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter

import fitz
from tkinter.filedialog import askopenfilename
from title import dis_title

#  打开PDF文件，生成一个对象
doc = fitz.open("a.pdf")
#pdf页数
page_numbers=doc.pageCount

#%%
title_index=[]
part_nums=[]
for i in range(doc.pageCount):
    page = doc[i]
    # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
    zoom_x = 4
    zoom_y = 4
    trans = fitz.Matrix(zoom_x, zoom_y).preRotate(0)
    pix = page.getPixmap(matrix=trans, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    #莱文斯坦距离,两个字符串的编辑距离
    flag,text=dis_title(img)
    print("页面{},识别到的文本:{}，是否是封面:{}".format(i,text,flag))
    if flag==True:
        title_index.append(i)
        #输入PIL格式的图片，返回零件号大概区域的截图
        probably=detectTable(img)
        #返回零件号精确区域的截图
        accurate=extract_part(probably)
        #ocr识别零件号
        part_No=tran_text(accurate)
        #查询数据库识别机种
        models=Judge(part_No)

        part_nums.append([part_No,models])
        print(part_No,"\n")

path=os.path.dirname(__file__)
output=os.path.join(path,"output")
#清空所有文件夹及其内部的文件
shutil.rmtree(os.path.join(output,"2WB"))
os.mkdir(os.path.join(output,"2WB"))
shutil.rmtree(os.path.join(output,"2HX"))
os.mkdir(os.path.join(output,"2HX"))
shutil.rmtree(os.path.join(output,"2LD"))
os.mkdir(os.path.join(output,"2LD"))
shutil.rmtree(os.path.join(output,"2QJ"))
os.mkdir(os.path.join(output,"2QJ"))
shutil.rmtree(os.path.join(output,"2SV"))
os.mkdir(os.path.join(output,"2SV"))
shutil.rmtree(os.path.join(output,"2YS"))
os.mkdir(os.path.join(output,"2YS"))
shutil.rmtree(os.path.join(output,"2VP"))
os.mkdir(os.path.join(output,"2VP"))
shutil.rmtree(os.path.join(output,"unknow"))
os.mkdir(os.path.join(output,"unknow"))


pdf = PdfFileReader("a.pdf")

#提取pdf的i~f页生成一个新的pdf
def gen_pdf(pdf,start,end):
    pdf_new = PdfFileWriter()
    for i in range(start,end):
        pdf_new.addPage(pdf.getPage(i))
    return pdf_new

# %%
for i,j in enumerate(title_index):
    if i<len(title_index)-1:
        start=title_index[i]
        end=title_index[i+1]-1
    else:
        start=title_index[i]
        end=page_numbers-1
    part_pdf=gen_pdf(pdf,start,end)

    part_No,models=part_nums[i]
    for y in models:
        savepath=os.path.join(output,y,part_No+".pdf")
        print("生成pdf文件:",savepath)
        file=open(savepath,'wb')
        part_pdf.write(file)
        file.close()
