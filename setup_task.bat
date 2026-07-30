@echo off
REM ============================================================
REM  Registers a Windows Scheduled Task that runs wallpaper_rotator.py
REM  every 6 hours, starting at midnight. Right-click this file and
REM  choose "Run as administrator" to install it.
REM
REM  To change to DAILY instead of every 6 hours, edit the
REM  /sc and /mo lines below (a commented DAILY version is included).
REM ============================================================

set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%wallpaper_rotator.py

echo Locating pythonw.exe (no console window on run)...
for /f "delims=" %%i in ('where pythonw') do set PYTHONW=%%i

if "%PYTHONW%"=="" (
    echo Could not find pythonw.exe on PATH. Make sure Python is installed
    echo and added to PATH, then try again.
    pause
    exit /b 1
)

echo Creating scheduled task "WallpaperRotator" (every 6 hours)...
schtasks /create /tn "WallpaperRotator" /tr "\"%PYTHONW%\" \"%SCRIPT_PATH%\"" /sc HOURLY /mo 6 /st 00:00 /f

REM ---- DAILY VERSION (comment the line above, uncomment below) ----
REM schtasks /create /tn "WallpaperRotator" /tr "\"%PYTHONW%\" \"%SCRIPT_PATH%\"" /sc DAILY /st 08:00 /f

echo.
echo Done! The task "WallpaperRotator" is now scheduled.
echo You can view/edit it anytime in Task Scheduler (taskschd.msc).
echo.
pause
