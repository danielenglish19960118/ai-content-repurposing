@echo off
chcp 65001 >nul
echo 正在尋找並執行 Python 程式...

:: 嘗試用 py 啟動器
py script.py
if %errorlevel% equ 0 goto end

:: 嘗試直接用 python
python script.py
if %errorlevel% equ 0 goto end

:: 如果上面兩者都失敗，手動尋找常見的 Python 安裝路徑
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe script.py
if %errorlevel% equ 0 goto end

C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe script.py
if %errorlevel% equ 0 goto end

echo.
echo [錯誤] 找不到可以執行的 Python，請確認程式檔名是否為 script.py
:end
pause