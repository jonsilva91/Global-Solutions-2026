# Astra Resilience Copilot - Run Script
# PowerShell script to run the FastAPI backend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Astra Resilience Copilot - Starting API" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "✗ Virtual environment not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Start the API server
Write-Host ""
Write-Host "Starting FastAPI server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "API will be available at:" -ForegroundColor Green
Write-Host "  • Main API: http://localhost:8000" -ForegroundColor White
Write-Host "  • Swagger UI: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  • ReDoc: http://localhost:8000/redoc" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run from project root
uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000

# Made with Bob
