Write-Host "Starting Gurukul Platform..." -ForegroundColor Green

Set-Location "c:\Users\Microsoft\Documents\Gurukul_new-main\Gurukul_new-main"

Write-Host "[1/2] Starting Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\Microsoft\Documents\Gurukul_new-main\Gurukul_new-main\Backend'; python main.py"

Start-Sleep -Seconds 3

Write-Host "[2/2] Starting Frontend..." -ForegroundColor Yellow  
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\Microsoft\Documents\Gurukul_new-main\Gurukul_new-main\new frontend'; npm run dev"

Write-Host "Both services are starting..." -ForegroundColor Green
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan