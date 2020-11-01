#import onnxruntime as rt
import  numpy as np
import time
import cv2
import os
import sys
path1=os.path.dirname(__file__)
path2=os.path.dirname(path1)
sys.path.append(path1)
sys.path.append(path2)
from decode import  SegDetectorRepresenter
from utils import get_rotate_crop_image

mean = (0.485, 0.456, 0.406)
std = (0.229, 0.224, 0.225)


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


class SingletonType(type):
    def __init__(cls, *args, **kwargs):
        super(SingletonType, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)
        cls.__init__(obj, *args, **kwargs)
        return obj


def draw_bbox(img_path, result, color=(255, 0, 0), thickness=2):
    if isinstance(img_path, str):
        img_path = cv2.imread(img_path)
        # img_path = cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB)
    img_path = img_path.copy()
    for point in result:
        point = point.astype(int)

        cv2.polylines(img_path, [point], True, color, thickness)
    return img_path


def coss_multi(v1, v2):
    """
    计算两个向量的叉乘
    :param v1:
    :param v2:
    :return:
    """
    return v1[0]*v2[1] - v1[1]*v2[0]

#计算矩形的面积
def polygon_area(box_list):
    areas=[]
    for polygon in box_list:
        n = len(polygon) 
        if n < 3:
            area=0
        vectors = np.zeros((n, 2))
        for i in range(0, n):
            vectors[i, :] = polygon[i, :] - polygon[0, :]
        area = 0
        for i in range(1, n):
            area = area + coss_multi(vectors[i-1, :], vectors[i, :]) / 2
        areas.append(area)
    return areas


class DBNET(metaclass=SingletonType):
    def __init__(self, MODEL_PATH):
        #self.sess = rt.InferenceSession(MODEL_PATH)
        self.sess = cv2.dnn.readNet(MODEL_PATH)

        self.decode_handel = SegDetectorRepresenter()

    def process(self, img, short_size):

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img.shape[:2]
        if h < w:
            scale_h = short_size / h
            tar_w = w * scale_h
            tar_w = tar_w - tar_w % 32
            tar_w = max(32, tar_w)
            scale_w = tar_w / w

        else:
            scale_w = short_size / w
            tar_h = h * scale_w
            tar_h = tar_h - tar_h % 32
            tar_h = max(32, tar_h)
            scale_h = tar_h / h
        


        img = cv2.resize(img, None, fx=scale_w, fy=scale_h)

        img = img.astype(np.float32)

        img /= 255.0
        img -= mean
        img /= std
        img = img.transpose(2, 0, 1)
        transformed_image = np.expand_dims(img, axis=0)
        #out = self.sess.run(["out1"], {"input0": transformed_image.astype(np.float32)})
        out = self.sess.setInput(transformed_image.astype(np.float32))
        out = [self.sess.forward()]

        
        
        box_list, score_list = self.decode_handel(out[0][0], h, w)
        if len(box_list) > 0:
            idx = box_list.reshape(box_list.shape[0], -1).sum(axis=1) > 0  # 去掉全为0的框
            box_list, score_list = box_list[idx], score_list[idx]
        else:
            box_list, score_list = [], []
        return box_list, score_list


if __name__ == "__main__":
    text_handle = DBNET(MODEL_PATH="../models/dbnet.onnx")
    img = cv2.imread(r"D:\hewei\soft\check report2\general_crop\general0.jpg")
    print(img.shape)
    #short_size:压缩图片的短边尺寸，只能是32的整数倍
    #box_list是box 4点坐标的numpy矩阵,shape=(n,4,2)
    #score_list是各个box的置信度
    box_list, score_list = text_handle.process(img,short_size=32*6)
    print("置信度",score_list)
    img2 = draw_bbox(img, box_list)
    cv2.imshow("test.jpg", img2)

    area=polygon_area(box_list)
    index=area.index(max(area))
    print("box面积:",polygon_area(box_list))
    #截取box区域的图片
    crop_img = get_rotate_crop_image(img, box_list[index].astype(np.float32))
    cv2.imshow("crop_img",crop_img)
