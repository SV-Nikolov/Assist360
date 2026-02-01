@echo off
REM Fusion 360 Copilot Assistant - Application Launcher
REM This batch file launches Fusion 360 with the Copilot add-in loaded

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Launch PowerShell with the launcher script
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%LAUNCHER.ps1" %*

REM Capture exit code
set EXIT_CODE=!ERRORLEVEL!

REM Exit with same code
exit /b !EXIT_CODE!
