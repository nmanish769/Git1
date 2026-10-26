@echo off
cd /d "%~dp0"
echo =================================================================
echo 🎓 Starting OpenLearn AI Full-Stack Web App (FastAPI + Frontend)
echo =================================================================
echo URL: http://localhost:8000
echo.

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py main.py
) else (
    python main.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠️ Launch failed. Attempting to install requirements...
    py -m pip install -r requirements.txt 2>nul || python -m pip install -r requirements.txt
    py main.py 2>nul || python main.py
)
pause
