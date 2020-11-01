# -*- coding: UTF-8 -*-
from PIL import Image as Img
import os
import sys
import pprint



def div_pages(x):
    im=Img.open(x)
    i=0
    pages=[]
    uppages=[]
    print("开始提取各页图片")
    try:
        while 1:
            part1 = im.crop((0, 0, 2473, 751))
            path=os.path.dirname(__file__)
            uppage=os.path.join(path,"uppages","uppage"+str(i)+".png")
            part1.save(uppage)
            uppages.append(uppage)
            page=os.path.join(path,"pages","page"+str(i)+".png")
            im.save(page)
            pages.append(page)
            print(i)
            #part1.show()
            #翻页
            im.seek(im.tell()+1)
            i=i+1
    except EOFError:
        pass
    return i,pages,uppages


if __name__=="__main__":
    os.chdir(sys.path[0])
    #file=os.path.join(path,"tiqu.tif")
    a=div_pages("tiqu.tif")
    pprint.pprint(a)

