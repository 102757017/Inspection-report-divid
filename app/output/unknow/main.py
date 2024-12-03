 # -*- coding: UTF-8 -*-
import os
import sys
import shutil
import re
import pprint
from judge import Judge_W,Judge_T

#将该文件放置到unknown文件夹内运行

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(bundle_dir)

obj_root=os.path.dirname(bundle_dir)
obj=os.path.join(bundle_dir,"output")
list_dirs=os.path.join(bundle_dir,"input")


for root,dirs,files in os.walk(bundle_dir):
    for name in files:
        if os.path.splitext(name)[1]=='.pdf':
            file_path=os.path.join(root,name)
            models=Judge_T(os.path.splitext(name)[0])
            
            #替换旧机种为新机种
            for i,m in enumerate(models):
                if m=="2SV":
                    models[i]="2VH"
                if m=="2HX":
                    models[i]="2HY"
                if m=="2LD":
                    models[i]="2LQ"
                if m=="2QJ":
                    models[i]="2QX"
                if m=="2FW":
                    models[i]="3FA"
            for m in models:
                obj=os.path.join(obj_root,m,name)
                print("正在处理",file_path)
                shutil.copy(file_path,obj)
