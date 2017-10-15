echo "如果出现FATALITIES错误,意味着某个字的块没找到，要么是坐标错误，要么是字符图像出了问题。如果字符没有可供使用的样本，它就不能被识别，那么得到的inttemp文件和unicharset文件就不匹配，Tesseract会退出。"
D:
cd %~dp0

echo Run Tesseract for Training..  
"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe" "%~dp0\part.no.tif" "%~dp0\part.no" box.train