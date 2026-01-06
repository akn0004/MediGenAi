@echo off
echo ========================================
echo MediGenAI Setup Script
echo ========================================
echo.

REM Check if virtual environment exists
if exist "venv" (
    echo Virtual environment already exists.
) else (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Copy .env.example to .env if it doesn't exist
if exist ".env" (
    echo .env file already exists.
) else (
    echo Creating .env file...
    copy .env.example .env
    echo Please update .env file with your database credentials!
)

echo.
echo ========================================
echo Database Setup
echo ========================================
echo.
echo Please make sure MySQL is running and you have created the database:
echo CREATE DATABASE medigenai_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
echo.
set /p continue="Have you created the database? (y/n): "

if /i "%continue%"=="y" (
    REM Run migrations
    echo Running migrations...
    python manage.py makemigrations
    python manage.py migrate

    REM Populate sample data
    echo Populating sample data...
    python manage.py populate_data

    echo.
    echo ========================================
    echo Setup Complete!
    echo ========================================
    echo.
    echo Default Login Credentials:
    echo   Username: admin
    echo   Password: admin123
    echo.
    echo To start the development server, run:
    echo   python manage.py runserver
    echo.
    echo Then open your browser to: http://localhost:8000
) else (
    echo Please create the database first and run this script again.
)

pause
