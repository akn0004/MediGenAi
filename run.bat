@echo off
echo ========================================
echo Starting MediGenAI Development Server
echo ========================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
    echo.
    
    REM Start the server
    echo Starting Django development server...
    echo Access the application at: http://localhost:8000
    echo Or from network: http://^<your-ip^>:8000
    echo Press CTRL+C to stop the server
    echo.
    python manage.py runserver 0.0.0.0:8000
) else (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to set up the project.
    pause
)
