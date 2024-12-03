cd /d %~dp0
%~dp0runtime\python %~dp0get-pip.py
set Path=%Path%;%~dp0Scripts
%~dp0runtime\python -m pip install setuptools
%~dp0runtime\python -m pip install paddlepaddle==2.6.2 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
%~dp0runtime\python -m pip install -r %~dp0\app\requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com

cmd /k echo.