@echo off
echo ========================================
echo   Committing Critical Fixes
echo ========================================

echo.
echo [1/3] Adding all changes...
git add -A

echo.
echo [2/3] Committing fixes...
git commit -m "CRITICAL FIXES: Synchronized fraud counts, fixed analytics filters for all graphs, unified Dashboard and Analytics data generation, added smart chatbot enhancement guide"

echo.
echo [3/3] Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   Fixes Pushed Successfully!
echo ========================================
pause
