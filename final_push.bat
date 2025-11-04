@echo off
git add .
git commit -m "Complete Enterprise Fraud Detection System with UiPath 2025 Integration and UI Improvements"
git remote remove origin
git remote add origin https://github.com/Sid1rahul/Enterprise-Fraud-Detection-System.git
git branch -M main
git push -f origin main
