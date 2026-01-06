# Setup script for MediGenAI
# Run this script to set up the project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MediGenAI Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
pip install -r requirements.txt

# Copy .env.example to .env if it doesn't exist
if (Test-Path ".env") {
    Write-Host ".env file already exists." -ForegroundColor Yellow
} else {
    Write-Host "Creating .env file..." -ForegroundColor Green
    Copy-Item ".env.example" ".env"
    Write-Host "Please update .env file with your database credentials!" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Database Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Please make sure MySQL is running and you have created the database:" -ForegroundColor Yellow
Write-Host "CREATE DATABASE medigenai_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" -ForegroundColor White
Write-Host ""
$continue = Read-Host "Have you created the database? (y/n)"

if ($continue -eq "y") {
    # Run migrations
    Write-Host "Running migrations..." -ForegroundColor Green
    python manage.py makemigrations
    python manage.py migrate

    # Populate sample data
    Write-Host "Populating sample data..." -ForegroundColor Green
    python manage.py populate_data

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Default Login Credentials:" -ForegroundColor Yellow
    Write-Host "  Username: admin" -ForegroundColor White
    Write-Host "  Password: admin123" -ForegroundColor White
    Write-Host ""
    Write-Host "To start the development server, run:" -ForegroundColor Yellow
    Write-Host "  python manage.py runserver" -ForegroundColor White
    Write-Host ""
    Write-Host "Then open your browser to: http://localhost:8000" -ForegroundColor Cyan
} else {
    Write-Host "Please create the database first and run this script again." -ForegroundColor Red
}
