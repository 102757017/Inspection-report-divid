# -*- coding: UTF-8 -*-
from PIL import Image
import sys
from crnn.CRNN import CRNNHandle

def tran_text(img):
    img=img.convert('RGB')
    crnn_handle = CRNNHandle(model_path="./models/crnn_lite_lstm.onnx")
    t=crnn_handle.predict_rbg(img)
    return t


if __name__=="__main__":
    img = Image.open(r"D:\hewei\soft\check report2\mistakepic\1534814862.jpg")
    t=tran_text(img)
    print("识别出文本:",t)
