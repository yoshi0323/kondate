@echo off
setlocal

REM Change to script directory
cd /d "%~dp0"

REM Set paths
set EXEFILE=kondate_system.exe

REM Check files
if not exist "%EXEFILE%" (
    echo ERROR: %EXEFILE% not found.
    goto :ERROR
)

REM Run the application
echo Starting application...
echo Please wait for browser to open...

start "" "%EXEFILE%"

echo Application running! Do not close this window.
echo Press Ctrl+C to quit.
cmd /k

:ERROR
echo Application could not start. Please check files.
pause
