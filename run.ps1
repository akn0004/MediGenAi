# Start MediGenAI Development Server

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting MediGenAI Development Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated" -ForegroundColor Green
    Write-Host ""
    
    # Start the server
    Write-Host "Starting Django development server..." -ForegroundColor Green
    Write-Host "Access the application at: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "Or from network: http://<your-ip>:8000" -ForegroundColor Cyan
    Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    python manage.py runserver 0.0.0.0:8000
} else {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first to set up the project." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
}
