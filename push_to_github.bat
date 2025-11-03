@echo off
echo ===== Starting Git Operations =====

echo.
echo 1. Setting up Git user...
git config --global user.email "sid1rahul@users.noreply.github.com"
git config --global user.name "sid1rahul"

echo.
echo 2. Adding all changes to staging...
git add .

echo.
echo 3. Committing changes...
git commit -m "🔧 Updated project with UiPath integration and UI improvements"

echo.
echo 4. Pushing to GitHub...
git push -u origin main

echo.
echo ===== Git Operations Complete =====
pause
