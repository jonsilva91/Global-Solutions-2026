# Astra Resilience Copilot - Setup Script
# PowerShell script to set up and run the FastAPI backend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Astra Resilience Copilot - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.10 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host ""
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Create data directory if it doesn't exist
Write-Host ""
Write-Host "Setting up data directory..." -ForegroundColor Yellow
if (-not (Test-Path "data/processed")) {
    New-Item -ItemType Directory -Path "data/processed" -Force | Out-Null
    Write-Host "✓ Data directory created" -ForegroundColor Green
} else {
    Write-Host "✓ Data directory already exists" -ForegroundColor Green
}

# Display success message
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the API server, run:" -ForegroundColor Yellow
Write-Host "  uvicorn src.backend.main:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "Or use the run script:" -ForegroundColor Yellow
Write-Host "  .\run.ps1" -ForegroundColor White
Write-Host ""
Write-Host "API will be available at:" -ForegroundColor Yellow
Write-Host "  http://localhost:8000" -ForegroundColor White
Write-Host "  http://localhost:8000/docs (Swagger UI)" -ForegroundColor White
Write-Host "  http://localhost:8000/redoc (ReDoc)" -ForegroundColor White
Write-Host ""

# Made with Bob
