@echo off
echo Starting Gurukul Platform...

cd "c:\Users\Microsoft\Documents\Gurukul_new-main\Gurukul_new-main"

echo [1/2] Starting Backend...
start "Gurukul Backend" cmd /k "cd Backend && python main.py"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend...
start "Gurukul Frontend" cmd /k "cd \"new frontend\" && npm run dev"

echo Both services starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
pause