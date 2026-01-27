@echo off
REM ================================================
REM 💧 Water Quality Chatbot - Windows Setup & Run
REM ================================================
REM Just double-click this file to run!
REM First run will install packages automatically.
REM ================================================

cd /d "%~dp0"

echo.
echo 💧 ==================================
echo    Water Quality Chatbot
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Please install Python first:
    echo   1. Go to https://www.python.org/downloads/
    echo   2. Download and install Python 3.9 or newer
    echo   3. IMPORTANT: Check "Add Python to PATH" during install
    echo   4. Run this script again
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check/Install dependencies
echo.
echo 📦 Checking dependencies...

python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo    Installing required packages (one-time^)...
    python -m pip install --upgrade pip --quiet
    python -m pip install streamlit pandas openpyxl netCDF4 --quiet
    echo    ✅ Packages installed!
) else (
    echo    ✅ All packages ready
)

REM Create data folder if needed
if not exist "data" mkdir data

REM Run the app
echo.
echo 🚀 Starting app...
echo    Opening in browser at http://localhost:8501
echo.
echo    ⚠️  Keep this window open while using the app!
echo    Press Ctrl+C to stop
echo.

python -m streamlit run app.py --server.headless=true

pause
