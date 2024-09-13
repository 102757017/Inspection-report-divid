import sys
import os
#os.system('''pip install paddlepaddle==2.2.2 paddleocr -i https://mirror.baidu.com/pypi/simple''')
from paddleocr import PaddleOCR, draw_ocr # pigar: required-packages=paddlepaddle
from PIL import Image
import fitz
from analysis_pic import detectTable
import cv2
import pprint

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
print("工作目录：",bundle_dir)
os.chdir(bundle_dir)


#输入矩形坐标例如[[101.0, 50.0], [585.0, 49.0], [585.0, 83.0], [101.0, 84.0]]，计算矩形面积
def area(rectangle):
    x1=rectangle[0][0]
    y1=rectangle[0][1]
    x2=rectangle[1][0]
    y2=rectangle[1][1]
    x3=rectangle[2][0]
    y3=rectangle[2][1]
    x4=rectangle[3][0]
    y4=rectangle[3][1]
    s=x1*y2+x2*y3+x3*y4+x4*y1-x2*y1-x2*y2-x4*y3-x4*y4
    return s




# use_angle_cls：是否加载方向分类模型
# use_space_char：是否识别空格
# rec_char_type：识别算法的字符类型，中英文(ch)、英文(en)、法语(french)、德语(german)、韩语(korean)、日语(japan)，默认为ch
# lang：模型语言类型,目前支持 目前支持中英文(ch)、英文(en)、法语(french)、德语(german)、韩语(korean)、日语(japan)，指定不同的语言会自动下载对应的预训练模型，下载路径为C:\Users\用户名\.paddleocr
# det_model_dir：自定义检测模型所在文件夹。自己转换好的inference模型路径，模型路径下必须包含model和params文件
# rec_model_dir：自定义识别模型所在文件夹。自己转换好的inference模型路径，模型路径下必须包含model和params文件
# rec_char_dict_path：自定义识别模型的字典路径。当rec_model_dir传参时需要修改为自己的字典路径
# cls_model_dir：自定义分类模型所在文件夹。自己转换好的inference模型路径，模型路径下必须包含model和params文件
# det_db_unclip_ratio 表示文本框的紧致程度，越小则文本框更靠近文本
# det_db_box_thresh DB后处理过滤box的阈值，如果检测存在漏框情况，可酌情减小
ocr_en = PaddleOCR(use_angle_cls=True, lang="en",det_db_unclip_ratio=2)
ocr_ch = PaddleOCR(use_angle_cls=True, lang="ch",use_space_char=True,use_gpu = False,det_db_unclip_ratio=2,det_db_box_thresh=0.1)


def tran_en(img):
    # cls:前向时是否启动分类
    result = ocr_en.ocr(img, cls=True)
    result2=[]
    if result[0] !=None:
        print(result)
        for index, item in enumerate(result[0]):
            s=area(item[0])
            #筛选文本框面积大的检测结果
            if s>10000:
                result2.append(item)
                
        for item in result2:
            print(item)

        # 保存识别结果的图片
        boxes = [line[0] for line in result2]
        txts = [line[1][0] for line in result2]
        scores = [line[1][1] for line in result2]
        im_show = draw_ocr(img, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/simfang.ttf')
        im_show = Image.fromarray(im_show)
        return result2,im_show
    else:
        return "",None


def tran_ch(img):
    # cls:前向时是否启动分类
    result = ocr_ch.ocr(img, cls=True)
    result2=[]
    if result[0] !=None:
        for index, item in enumerate(result[0]):
            s=area(item[0])
            #筛选文本框面积大的检测结果
            if s>11000:
                result2.append(item)
                
        for item in result2:
            print(item)

        # 保存识别结果的图片
        boxes = [line[0] for line in result2]
        txts = [line[1][0] for line in result2]
        scores = [line[1][1] for line in result2]
        im_show = draw_ocr(img, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/simfang.ttf')
        im_show = Image.fromarray(im_show)
        return result2,im_show
    else:
        return "",None    


if __name__=="__main__":
    #  打开PDF文件，生成一个对象
    file_name="2.pdf"
    doc = fitz.open(file_name)
    #第一页
    page = doc[8]
    # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
    zoom_x = 4
    zoom_y = 4  
    trans = fitz.Matrix(zoom_x, zoom_y).prerotate(0)
    pix = page.get_pixmap(matrix=trans, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    #输入PIL格式的图片，返回零件号大概区域的截图
    probably=detectTable(img)
    print(type(probably))
    #识别图片中的零件号
    result,img=tran_en(probably)
    img.save('./general_crop/result.jpg')
    print(result)
    


