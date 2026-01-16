@echo off
echo ========================================
echo   Medical Records System - 3-Tier
echo   Starting Server...
echo ========================================
echo.

REM Activate virtual environment if exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo No virtual environment found
)

echo.
echo Initializing database...
python init_db.py

echo.
echo Starting FastAPI server on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000
