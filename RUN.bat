@echo off
REM Fusion 360 Copilot Assistant - Test Runner
REM This batch file runs the PowerShell test suite

setlocal enabledelayedexpansion
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0RUN.ps1" %*
exit /b !ERRORLEVEL!
