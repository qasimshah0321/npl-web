@echo off
echo ==========================================
echo Pushing to GitHub
echo ==========================================
echo.
echo IMPORTANT: Replace YOUR_USERNAME with your actual GitHub username!
echo.
pause

cd /d "E:\Personal-projects\CludeCode\NPL Web"

REM Add GitHub remote (replace YOUR_USERNAME with your actual username)
git remote add origin https://github.com/YOUR_USERNAME/npl-web.git

REM Rename branch to main
git branch -M main

REM Push to GitHub
git push -u origin main

echo.
echo ==========================================
echo Done! Your code is now on GitHub
echo ==========================================
pause
