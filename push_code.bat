@echo off
echo ==========================================
echo   PRAJA SAHAYAKA - GITHUB PUSH SCRIPT
echo ==========================================

echo.
echo [1/5] Checking for Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is NOT installed. Installing now via Winget...
    winget install -e --id Git.Git
    echo.
    echo ================================================================
    echo CRITICAL: Git was just installed. 
    echo You MUST close this window and run the file again for it to work.
    echo ================================================================
    pause
    exit
) else (
    echo Git is installed. Proceeding...
)

echo.
echo [2/5] Initializing Repository...
git init

echo.
echo [3/5] Adding Files...
git add .
git commit -m "Final Submission"

echo.
echo [4/5] Configuring Remote...
git branch -M main
:: Remove origin if it exists to avoid errors
git remote remove origin 2>nul
git remote add origin https://github.com/2100080051/praja-sahayaka.git

echo.
echo [5/5] Pushing to GitHub...
echo (A window may pop up asking you to sign in to GitHub)
git push -u origin main

echo.
echo ==========================================
echo             DONE!
echo ==========================================
pause
