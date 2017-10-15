echo "»¶Ó­!"
D:
cd %~dp0
echo Run Tesseract for Training..  
"C:\Program Files (x86)\Tesseract-OCR\shapeclustering.exe" -F "%~dp0\font_properties" -U "%~dp0\unicharset"  "%~dp0\part.no.tr"