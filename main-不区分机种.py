 # -*- coding: UTF-8 -*-
from PIL import Image as Img
import os
import pprint
import sys
import cv2

sys.path.append(os.path.dirname(__file__))
from tifdiv import div_pages
from title import title_page,comp
from title import splitpage
from analysis_pic import detectTable
from analysis_pic import extract_part
from ocr import tran_text
from topdf import imgtopdf
from judge import Judge


path=os.path.dirname(__file__)
file=os.path.join(path,"tiqu.tif")
#返回总页数，各page路径列表，各uppage路径列表
a=div_pages(file)
page_num=a[0]
pages=a[1]
uppages=a[2]

title=title_page(uppages)

#返回封面页码列表
title_num=title[0]


#返回封面路径列表
title_path=title[1]

pdfs=splitpage(pages,title_num)
pprint.pprint(pdfs)

part_nums=[]
for index,x in enumerate(title_num):  
    print(pages[x])
    #返回零件号大概区域的截图  
    general_crop=detectTable(pages[x])
    general_img=os.path.join(os.path.dirname(__file__),"general_crop",'general'+str(index)+'.jpg')
    cv2.imwrite(general_img,general_crop)
    
    #返回零件号的精确截图
    accurate_crop=extract_part(general_crop)
    name_img=os.path.join(os.path.dirname(__file__),"accurate_crop",'part'+str(index)+'.jpg')
    #保存零件号截图
    cv2.imwrite(name_img,accurate_crop)    
    #识别图片零件号
    part_num=tran_text(name_img)
    part_nums.append(part_num)


print(part_nums)
print(pdfs)
output=os.path.join(path,"output")
for index,x in enumerate(pdfs):
    print(type(part_nums[index]),part_nums[index])
    savepath=os.path.join(output,part_nums[index]+".pdf")
    print("生成pdf文件:",savepath)
    imgtopdf(x,savepath)
    
