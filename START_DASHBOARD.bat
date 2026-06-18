@echo off
title SIRTI Dashboard Launcher
color 0A

echo ==========================================
echo   SIRTI DASHBOARD LAUNCHER
echo   Vodafone Qatar Field Operations
echo ==========================================
echo.

REM Find the script directory
set SCRIPT_DIR=%~dp0

echo [1/3] Checking for dashboard file...
if exist "%SCRIPT_DIR%sirti_dashboard_final.py" (
    echo     FOUND: sirti_dashboard_final.py
    set DASHBOARD=%SCRIPT_DIR%sirti_dashboard_final.py
    goto CHECK_PYTHON
)

if exist "%SCRIPT_DIR%sirti_dashboard_v2.py" (
    echo     FOUND: sirti_dashboard_v2.py
    set DASHBOARD=%SCRIPT_DIR%sirti_dashboard_v2.py
    goto CHECK_PYTHON
)

if exist "%SCRIPT_DIR%sirti_dashboard.py" (
    echo     FOUND: sirti_dashboard.py
    set DASHBOARD=%SCRIPT_DIR%sirti_dashboard.py
    goto CHECK_PYTHON
)

echo     ERROR: No dashboard file found!
echo     Looking for: sirti_dashboard_final.py
echo     Current folder: %SCRIPT_DIR%
pause
exit /b 1

:CHECK_PYTHON
echo.
echo [2/3] Checking Python installation...

python -m pip --version >nul 2>&1
if %errorlevel% == 0 (
    echo     Python found: OK
    set PYTHON_CMD=python
    goto CHECK_PACKAGES
)

py -3 -m pip --version >nul 2>&1
if %errorlevel% == 0 (
    echo     Python found via py launcher: OK
    set PYTHON_CMD=py -3
    goto CHECK_PACKAGES
)

echo     ERROR: Python not found!
echo     Please install Python from https://python.org/downloads
echo     IMPORTANT: Check "Add Python to PATH" during installation!
pause
exit /b 1

:CHECK_PACKAGES
echo.
echo [3/3] Checking required packages...

%PYTHON_CMD% -c "import streamlit" >nul 2>&1
if %errorlevel% == 0 (
    echo     Streamlit: OK
) else (
    echo     Installing Streamlit...
    %PYTHON_CMD% -m pip install streamlit plotly pandas
)

%PYTHON_CMD% -c "import plotly" >nul 2>&1
if %errorlevel% == 0 (
    echo     Plotly: OK
) else (
    echo     Installing Plotly...
    %PYTHON_CMD% -m pip install plotly
)

%PYTHON_CMD% -c "import pandas" >nul 2>&1
if %errorlevel% == 0 (
    echo     Pandas: OK
) else (
    echo     Installing Pandas...
    %PYTHON_CMD% -m pip install pandas
)

echo.
echo ==========================================
echo   LAUNCHING DASHBOARD...
echo ==========================================
echo.
echo The dashboard will open in your browser.
echo URL: http://localhost:8501
echo.
echo Press Ctrl+C in this window to stop.
echo.

%PYTHON_CMD% -m streamlit run "%DASHBOARD%"

pause