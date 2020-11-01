# -*- coding: UTF-8 -*-
from PIL import Image
import sys
import pytesseract
import os


def tran_text(file_path):
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" -psm 7'
    '''
    -psm N 
    将Tesseract设置为仅运行布局分析的一个子集并假定某种形式的图像。N的选项有：
    0 =仅定向和脚本检测（OSD）。
    1 =自动页面分割与OSD。
    2 =自动页面分割，但没有OSD或OCR。
    3 =全自动页面分割，但没有OSD。（默认）
    4 =假设单列可变大小的文本。
    5 =假设垂直排列文本的单个统一块。
    6 =假设单个统一的文本块。
    7 =将图像视为单个文本行。
    8 =将图像视为单个字。
    9 =将图像视为一个单一的单词。
    10 =将图像视为单个字符。
    '''
    im = Image.open(file_path)
    #part为“C:\Program Files (x86)\Tesseract-OCR\tessdata”目录下训练过的语言文件
    t=pytesseract.image_to_string(im,lang="part",config=tessdata_dir_config)
    print("识别到零件号:",t)
    
    return t


if __name__=="__main__":
    os.chdir(sys.path[0])
    tran_text(r"H:\学习资料\编程学习\pathon\基础操作\检查成绩书转PDF\mistakepic\1519729569.jpg")
