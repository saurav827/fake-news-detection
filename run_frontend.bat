@echo off
title Frontend - Fake News Detection

echo =================================
echo Starting Streamlit Frontend...
echo Frontend Running: 
echo http://localhost:8501
echo =================================
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment (.venv) missing!
    echo Please create it and install requirements.
    pause
    exit /b
)

call .venv\Scripts\activate.bat

echo Starting Streamlit app...
:: Streamlit automatically opens the browser window by default on Windows
python -m streamlit run app.py --server.port 8501

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Frontend crashed or failed to start.
    echo Make sure no other program is using port 8501.
)

pause
