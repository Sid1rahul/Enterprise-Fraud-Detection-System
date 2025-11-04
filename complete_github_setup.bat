@echo off
echo ========================================
echo   GitHub Repository Setup and Push
echo ========================================

echo.
echo [1/6] Configuring Git user...
git config user.email "sid1rahul@users.noreply.github.com"
git config user.name "Sid1rahul"

echo.
echo [2/6] Checking current Git status...
git status

echo.
echo [3/6] Adding all files to staging...
git add -A

echo.
echo [4/6] Committing changes...
git commit -m "Complete Enterprise Fraud Detection System with UiPath Integration"

echo.
echo [5/6] Setting up remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/Sid1rahul/Enterprise-Fraud-Detection-System.git

echo.
echo [6/6] Pushing to GitHub (main branch)...
git branch -M main
git push -f origin main

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Repository: https://github.com/Sid1rahul/Enterprise-Fraud-Detection-System
echo.
pause
