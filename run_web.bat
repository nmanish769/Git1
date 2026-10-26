@echo off
cd /d "%~dp0"
echo =================================================================
echo 🎓 Starting OpenLearn AI Full-Stack Web App (FastAPI + Frontend)
echo =================================================================
echo URL: http://localhost:8000
echo.
py main.py
if %ERRORLEVEL% NEQ 0 (
    python main.py
)
pause
