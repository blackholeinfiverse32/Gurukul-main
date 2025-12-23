@echo off
echo ========================================
echo Starting AnimateDiff API Server
echo ========================================
echo.

cd /d "%~dp0"

REM Activate venv if it exists
if exist "..\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "..\venv\Scripts\activate.bat"
)

echo Checking Python...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing/updating dependencies...
pip install omegaconf fastapi uvicorn python-multipart diffusers transformers -q

echo.
echo Starting AnimateDiff API Server on port 8501...
echo.
echo NOTE: First startup may take several minutes to download models
echo       The server will be ready when you see "Application startup complete"
echo.

python api_server.py

pause








