@echo off
title Fake News Detection - One Click Startup

echo =================================
echo   Fake News Detection System
echo     One-Click Project Run
echo =================================
echo.
echo Launching Backend Server...
start "Backend - Fake News" cmd /c "run_backend.bat"

echo Waiting 3 seconds for Backend to start...
timeout /t 3 /nobreak >nul

echo Launching Frontend Server...
start "Frontend - Fake News" cmd /c "run_frontend.bat"

echo.
echo =================================
echo Project started successfully!
echo The browser should open automatically.
echo You can safely close this launcher terminal.
echo =================================
timeout /t 3 >nul
