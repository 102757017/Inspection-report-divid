 # -*- coding: UTF-8 -*-
import os
import sys
import shutil
import re
import pprint
from judge import Judge

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
            models=Judge(os.path.splitext(name)[0])
            for x in models:
                obj=os.path.join(obj_root,x,name)
                print("正在处理",file_path)
                shutil.copy(file_path,obj)
