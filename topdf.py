# -*- coding: UTF-8 -*-
import sys
from reportlab.lib.pagesizes import A4,portrait
from reportlab.pdfgen import canvas
import reportlab
import os


#input_paths:图片路径列表  outputpath:输出pdf的零件名和路径
def imgtopdf(input_paths,outputpath):
    #创建一个空的pdf,landscape(A4)表示横向A4大小,portrait(A4)表示竖向A4大小
    c=canvas.Canvas(outputpath,pagesize=portrait(A4))
    (maxw,maxh)=portrait(A4)
    for x in input_paths:
        #向PDF内插入图片
        c.drawImage(x,0,0,maxw,maxh)
        #showPage产生一个分页
        c.showPage()
    c.save()

#a=os.path.join(os.path.dirname(__file__),"output","output.pdf")

#imgtopdf([r"D:\check report\pages\page0.png",r"D:\check report\pages\page1.png"],a)
