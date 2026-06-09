# Astra Resilience Copilot - Frontend Runner
# This script starts the React Mission Console

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Astra Resilience Copilot" -ForegroundColor Cyan
Write-Host "Mission Console Frontend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend directory
Set-Location -Path "frontend/mission-console"

# Check if node_modules exists
if (-Not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
    Write-Host ""
}

# Start the development server
Write-Host "Starting React development server..." -ForegroundColor Green
Write-Host "Frontend will be available at: http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "Make sure the backend is running at: http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host ""

npm run dev

# Made with Bob
