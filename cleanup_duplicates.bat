@echo off
echo Cleaning up duplicate and redundant files...

REM Delete duplicate batch files
del /F /Q "PUSH_AFTER_REPO_CREATED.bat" 2>nul
del /F /Q "commit_critical_fixes.bat" 2>nul
del /F /Q "commit_voice_chatbot.bat" 2>nul
del /F /Q "commit_wake_word.bat" 2>nul
del /F /Q "complete_github_setup.bat" 2>nul
del /F /Q "final_commit_and_push.bat" 2>nul
del /F /Q "final_push.bat" 2>nul
del /F /Q "git_commit.bat" 2>nul
del /F /Q "git_commit_new.bat" 2>nul
del /F /Q "push_enhancements.bat" 2>nul
del /F /Q "push_to_github.bat" 2>nul

REM Delete duplicate/old documentation
del /F /Q "NOVEL_IMPROVEMENTS_ROADMAP.md" 2>nul
del /F /Q "UiPath_Browser_Fix.md" 2>nul
del /F /Q "UIPATH_INTEGRATION_GUIDE.md" 2>nul
del /F /Q "UIPATH_SETUP_INSTRUCTIONS.md" 2>nul
del /F /Q "UiPath_Manual_Setup_Guide.md" 2>nul
del /F /Q "UiPath_Simple_Workflow.md" 2>nul
del /F /Q "UIPATH_STUDIO_2025_INTEGRATION.md" 2>nul
del /F /Q "SMART_CHATBOT_ENHANCEMENT.md" 2>nul
del /F /Q "GITHUB_SETUP.md" 2>nul
del /F /Q "FUTURE_IMPROVEMENTS_ROADMAP.md" 2>nul
del /F /Q "FINAL_SUMMARY.md" 2>nul
del /F /Q "PROJECT_WORKFLOW_PRESENTATION.md" 2>nul
del /F /Q "PROJECT_REVIEW_QA.md" 2>nul
del /F /Q "PROJECT_COMPLETION_SUMMARY.md" 2>nul
del /F /Q "PRE_COMMIT_SUMMARY.md" 2>nul
del /F /Q "FEATURE_TESTING_CHECKLIST.md" 2>nul
del /F /Q "ENHANCEMENT_IDEAS.md" 2>nul
del /F /Q "REAL_TIME_MONITORING_GUIDE.md" 2>nul
del /F /Q "UIPATH_CONNECTION_SUMMARY.md" 2>nul
del /F /Q "API_TESTING_SUMMARY.md" 2>nul
del /F /Q "COMPREHENSIVE_PROJECT_DOCUMENTATION.md" 2>nul
del /F /Q "CURL_API_TESTING_GUIDE.md" 2>nul
del /F /Q "WAKE_WORD_QUICK_START.txt" 2>nul

echo Cleanup complete!
pause
