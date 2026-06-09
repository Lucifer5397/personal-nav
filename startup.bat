@echo off
:: 个人导航中心 - 开机启动脚本
:: 等待MySQL服务启动完毕
timeout /t 5 /nobreak >nul
:: 确保使用正确的Python
set PYTHON=C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe
:: 启动Flask（最小化窗口）
cd /d E:\works\web-app
start "" /min "%PYTHON%" -u app.py
