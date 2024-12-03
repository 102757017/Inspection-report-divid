import cv2  
from paddleocr import PaddleOCR  
  
# 初始化OCR模型  
ocr = PaddleOCR(use_gpu=False)  
  
# 读取文档图像  
image_path = 'bbb.jpg'  
image = cv2.imread(image_path)  
  
# 使用OCR模型检测文档的倾斜角度  
result = ocr.ocr(image)  


print(result)
