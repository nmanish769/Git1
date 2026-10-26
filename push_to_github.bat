@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo =================================================================
echo 🚀 OpenLearn AI — Automated GitHub Sync
echo Repository: https://github.com/nmanish769/Git1.git
echo =================================================================
echo.

:: 1. Verify Git Installation
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ ERROR: Git is not installed or not in PATH!
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

:: 2. Initialize repo if needed
if not exist ".git" (
    echo 📦 Initializing local Git repository...
    git init
)

:: 3. Configure Remote URL safely
git remote set-url origin https://github.com/nmanish769/Git1.git 2>nul
if %ERRORLEVEL% NEQ 0 (
    git remote add origin https://github.com/nmanish769/Git1.git 2>nul
)

:: 4. Ensure branch is main
git branch -M main

:: 5. Stage ALL files (Frontend, Backend, Configs, Assets)
echo 📂 Staging all project files (frontend, backend, scripts, docs)...
git add -A

:: 6. Commit changes only if there are changes staged
git diff --cached --quiet
if %ERRORLEVEL% NEQ 0 (
    echo 💾 Committing updates...
    git commit -m "Update OpenLearn AI full-stack structure, AI model links, and doubt solver"
) else (
    echo ℹ️ Working tree is clean (no new changes to commit).
)

:: 7. Push to GitHub main branch
echo 🚀 Pushing to GitHub (https://github.com/nmanish769/Git1.git)...
git push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ Standard push failed, attempting safe push with upstream tracking...
    git push -u origin main --force
)

echo.
echo =================================================================
echo ✅ OpenLearn AI successfully pushed to GitHub!
echo 🌐 Live Website: https://nmanish769.github.io/Git1/
echo 📁 Repository:   https://github.com/nmanish769/Git1
echo =================================================================
echo.
pause
