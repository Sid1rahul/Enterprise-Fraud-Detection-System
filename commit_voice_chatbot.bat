@echo off
echo ========================================
echo   Committing Voice-Enabled Chatbot
echo ========================================

echo.
echo [1/3] Adding all changes...
git add -A

echo.
echo [2/3] Committing...
git commit -m "Add WhatsApp-style voice recording to chatbot with improved NLP and complete UiPath workflow guide"

echo.
echo [3/3] Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   Voice Chatbot Pushed Successfully!
echo ========================================
pause
