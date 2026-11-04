@echo off
chcp 65001 >nul
echo ========================================================
echo   InsightEngine Enterprise AI SaaS - Startup Launcher
echo ========================================================

:: Check for py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto check_env
)

:: Check for direct python command
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto check_env
)

echo.
echo [ERROR] Python interpreter not found! Please ensure Python 3.11+ is installed and added to PATH.
pause
exit /b 1

:check_env
echo [+] Validating and installing dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt --quiet

echo [+] Launching InsightEngine Streamlit Application...
%PYTHON_CMD% -m streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
pause
