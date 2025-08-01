@echo off
REM Launch script for ARRI MXF Recovery Tool (Windows)

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3 to run this tool
    pause
    exit /b 1
)

REM Change to script directory
cd /d "%SCRIPT_DIR%"

REM Run the tool
python main.py