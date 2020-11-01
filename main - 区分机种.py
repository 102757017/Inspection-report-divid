 # -*- coding: UTF-8 -*-
from PIL import Image as Img
import os
import pprint
import sys
import cv2
import shutil

sys.path.append(os.path.dirname(__file__))
from tifdiv import div_pages
from title import title_page,comp
from title import splitpage
from analysis_pic import detectTable
from analysis_pic import extract_part
from ocr import tran_text
from topdf import imgtopdf
from judge import Judge


os.chdir(sys.path[0])

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

#返回各pdf构成分页的图片路径列表
pdfs=splitpage(pages,title_num)
pprint.pprint(pdfs)

part_nums=[]
for index,x in enumerate(title_num):  
    print(pages[x])
    #返回零件号大概区域的截图  
    general_crop=detectTable(pages[x])
    general_img=os.path.join(os.path.dirname(__file__),"general_crop",'general'+str(index)+'.jpg')

    #cv2.imwrite(general_img,general_crop)
    #由于cv2.imwrite不支持保存图片到中文路径，用以下方法代替cv2.imwrite
    cv2.imencode('.jpg', general_crop)[1].tofile(general_img)
    
    #返回零件号的精确截图
    accurate_crop=extract_part(general_crop)
    name_img=os.path.join(os.path.dirname(__file__),"accurate_crop",'part'+str(index)+'.jpg')

    #保存零件号截图
    #cv2.imwrite(name_img,accurate_crop)
    #由于cv2.imwrite不支持保存图片到中文路径，用以下方法代替cv2.imwrite
    cv2.imencode('.jpg', accurate_crop)[1].tofile(name_img)    

    #识别图片零件号
    part_num=tran_text(name_img)
    models=Judge(part_num)
    part_nums.append([part_num,models])


output=os.path.join(path,"output")
#清空所有文件夹及其内部的文件
shutil.rmtree(os.path.join(output,"2GW"))
os.mkdir(os.path.join(output,"2GW"))
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
shutil.rmtree(os.path.join(output,"DS1"))
os.mkdir(os.path.join(output,"DS1"))
shutil.rmtree(os.path.join(output,"unknow"))
os.mkdir(os.path.join(output,"unknow"))


print(part_nums)
print(pdfs)
for index,x in enumerate(pdfs):
    for y in part_nums[index][1]:
        savepath=os.path.join(output,y,part_nums[index][0]+".pdf")
        print("生成pdf文件:",savepath)
        imgtopdf(x,savepath)
    
