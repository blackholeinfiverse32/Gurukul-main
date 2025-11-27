@echo off
title Gurukul - All Services
color 0A

echo ========================================
echo   STARTING ALL GURUKUL SERVICES
echo ========================================
echo.

REM Start Main Backend (Port 8000)
echo [1/3] Starting Main Backend (Port 8000)...
cd "Gurukul_new-main\Backend"
start "Backend-8000" cmd /k "python main.py"
timeout /t 3 /nobreak >nul

REM Start Chatbot Service (Port 8001)
echo [2/3] Starting Chatbot Service (Port 8001)...
cd "dedicated_chatbot_service"
start "Chatbot-8001" cmd /k "python chatbot_api.py"
cd ..
timeout /t 3 /nobreak >nul

REM Start Frontend (Port 5175)
echo [3/3] Starting Frontend (Port 5175)...
cd "..\new frontend"
start "Frontend-5175" cmd /k "npm run dev"
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   ALL SERVICES STARTED
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Chatbot:  http://localhost:8001
echo Frontend: http://localhost:5175
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:5175

echo.
echo Services running in separate windows.
echo Close windows to stop services.
pause
