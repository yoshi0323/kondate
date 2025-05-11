@echo off
echo Menu Management System
echo =====================
echo Starting application...

cd %~dp0
cd src
python run_app.py

if errorlevel 1 (
    echo An error occurred when starting the application.
    echo Please contact support if the problem persists.
    pause
) 