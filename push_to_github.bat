@echo off
cd /d "%~dp0"
echo =================================================================
echo 🚀 Pushing OpenLearn AI Full Project to GitHub
echo Repo: https://github.com/nmanish769/Git1.git
echo =================================================================
echo.

git init
git remote remove origin 2>nul
git remote add origin https://github.com/nmanish769/Git1.git
git branch -M main
git add .
git commit -m "Deploy full interactive OpenLearn AI with proper frontend, backend, and GitHub Pages"
git push -u origin main --force

echo.
echo =================================================================
echo ✅ Project successfully pushed to GitHub!
echo 🌐 GitHub Pages URL: https://nmanish769.github.io/Git1/
echo 📁 Repository:       https://github.com/nmanish769/Git1
echo =================================================================
pause
