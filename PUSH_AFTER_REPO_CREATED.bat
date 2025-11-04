@echo off
echo ========================================
echo   Pushing to GitHub
echo ========================================
echo.
echo Make sure you've created the repository:
echo https://github.com/Sid1rahul/Enterprise-Fraud-Detection-System
echo.
pause

git remote remove origin 2>nul
git remote add origin https://github.com/Sid1rahul/Enterprise-Fraud-Detection-System.git
git branch -M main
git push -u origin main

echo.
echo ========================================
echo   Push Complete!
echo ========================================
echo.
echo View your repository at:
echo https://github.com/Sid1rahul/Enterprise-Fraud-Detection-System
echo.
pause
