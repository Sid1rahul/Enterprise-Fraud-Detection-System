@echo off
echo ========================================
echo   Committing Wake Word Detection
echo ========================================

echo.
echo [1/3] Adding all changes...
git add -A

echo.
echo [2/3] Committing...
git commit -m "Add offline wake word detection 'Hey Fraud Detector' with visual indicators and complete guide"

echo.
echo [3/3] Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   Wake Word Feature Pushed!
echo ========================================
pause
