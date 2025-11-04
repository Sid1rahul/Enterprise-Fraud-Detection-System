@echo off
echo ========================================
echo   Final Commit and Push to GitHub
echo ========================================

echo.
echo [1/5] Adding all changes...
git add -A

echo.
echo [2/5] Committing with comprehensive message...
git commit -m "Complete Enterprise Fraud Detection System with UiPath 2025 Integration - Fixed analytics filtering, stable monitoring, dark theme notifications, comprehensive documentation"

echo.
echo [3/5] Setting up remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/Sid1rahul/Enterprise-Fraud-Detection-System.git

echo.
echo [4/5] Preparing main branch...
git branch -M main

echo.
echo [5/5] Pushing to GitHub...
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
