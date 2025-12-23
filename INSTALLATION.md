# Installation Instructions for MediGenAI

## System Requirements

- **Operating System**: Windows 10/11, Linux, or macOS
- **Python**: 3.8 or higher
- **MySQL**: 8.0 or higher
- **RAM**: Minimum 4GB
- **Disk Space**: At least 500MB free

## Part 1: Install Prerequisites

### 1.1 Install Python

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   ```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**macOS:**
```bash
brew install python3
```

### 1.2 Install MySQL

**Windows:**
1. Download MySQL Installer from https://dev.mysql.com/downloads/installer/
2. Choose "MySQL Installer for Windows"
3. Run installer and select "Developer Default"
4. Set root password during installation (remember this!)
5. Complete the installation

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

### 1.3 Verify MySQL is Running

**Windows:**
- Open Services (Win + R, type `services.msc`)
- Look for "MySQL80" - it should be "Running"

**Linux/macOS:**
```bash
sudo systemctl status mysql
```

## Part 2: Database Configuration

### 2.1 Create Database

**Option A: Using MySQL Command Line**

1. Open MySQL Command Line Client
2. Enter your root password
3. Run:
   ```sql
   CREATE DATABASE medigenai_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   SHOW DATABASES;
   EXIT;
   ```

**Option B: Using MySQL Workbench**

1. Open MySQL Workbench
2. Connect to your local instance
3. Click "Create a new schema" icon
4. Name: `medigenai_db`
5. Charset: `utf8mb4`
6. Collation: `utf8mb4_unicode_ci`
7. Click Apply

### 2.2 Create MySQL User (Optional but Recommended)

```sql
CREATE USER 'medigenai_user'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON medigenai_db.* TO 'medigenai_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## Part 3: Project Setup

### 3.1 Navigate to Project Directory

```bash
cd C:\Users\ecbin\Workspace\MediGenAi
```

### 3.2 Automated Setup (RECOMMENDED)

**For Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

**For Windows Command Prompt:**
```cmd
setup.bat
```

The script will handle everything automatically!

### 3.3 Manual Setup (If Automated Fails)

**Step 1: Create Virtual Environment**
```bash
python -m venv venv
```

**Step 2: Activate Virtual Environment**

Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

Windows CMD:
```cmd
venv\Scripts\activate.bat
```

Linux/macOS:
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt.

**Step 3: Upgrade pip**
```bash
python -m pip install --upgrade pip
```

**Step 4: Install Dependencies**
```bash
pip install -r requirements.txt
```

**If mysqlclient installation fails:**

Windows users may need Microsoft C++ Build Tools:
1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++"
3. Try installing again: `pip install mysqlclient`

Alternative: Use pre-built wheel
```bash
pip install wheel
# Download appropriate wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
pip install mysqlclient-xxx.whl
```

**Step 5: Configure Environment Variables**

```bash
copy .env.example .env
```

Edit `.env` file with your favorite text editor:

```ini
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
DEBUG=True
DB_NAME=medigenai_db
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_ROOT_PASSWORD
DB_HOST=localhost
DB_PORT=3306
```

**Step 6: Apply Database Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

You should see:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying reports.0001_initial... OK
```

**Step 7: Create Sample Data**
```bash
python manage.py populate_data
```

This creates:
- Admin user (username: admin, password: admin123)
- 10 sample patients
- Multiple medical reports

**Step 8: Create Additional Superuser (Optional)**
```bash
python manage.py createsuperuser
```

## Part 4: Run the Application

### 4.1 Start Development Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 4.2 Access the Application

Open your web browser and navigate to:
```
http://localhost:8000
```

or

```
http://127.0.0.1:8000
```

### 4.3 Login

Use the default credentials:
- **Username**: `admin`
- **Password**: `admin123`

## Part 5: Verification

After logging in, verify everything works:

1. ✅ Dashboard loads with statistics
2. ✅ You can see sample patients
3. ✅ Reports are visible
4. ✅ AI Analysis page shows charts
5. ✅ You can add a new patient

## Troubleshooting Guide

### Error: "python is not recognized"
**Solution:** Add Python to system PATH
1. Search for "Environment Variables" in Windows
2. Edit PATH variable
3. Add Python installation directory
4. Restart command prompt

### Error: "No module named 'django'"
**Solution:** Virtual environment not activated or packages not installed
```bash
# Activate venv first
.\venv\Scripts\Activate.ps1
# Then install
pip install -r requirements.txt
```

### Error: "Access denied for user"
**Solution:** Wrong MySQL credentials
- Check username/password in `.env` file
- Verify MySQL user has permissions
- Try using root user

### Error: "Can't connect to MySQL server"
**Solution:** MySQL service not running
- Windows: Check Services panel
- Linux: `sudo systemctl start mysql`

### Error: "Port 8000 already in use"
**Solution:** Use different port
```bash
python manage.py runserver 8080
```

### Error: "OperationalError: no such table"
**Solution:** Migrations not applied
```bash
python manage.py migrate
```

### Error: "Template does not exist"
**Solution:** Check TEMPLATES setting in settings.py
- Ensure templates directory exists
- Verify TEMPLATES DIRS configuration

## Uninstall / Clean Up

To remove the project:

1. Deactivate virtual environment:
   ```bash
   deactivate
   ```

2. Delete virtual environment:
   ```bash
   rmdir /s venv
   ```

3. Drop database:
   ```sql
   DROP DATABASE medigenai_db;
   ```

## Production Deployment Notes

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Generate strong SECRET_KEY
3. Update ALLOWED_HOSTS
4. Use environment-specific database
5. Configure static files serving
6. Use production WSGI server (Gunicorn)
7. Set up HTTPS
8. Configure firewall
9. Set up backups
10. Use environment variables for sensitive data

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- MySQL Documentation: https://dev.mysql.com/doc/
- Python Documentation: https://docs.python.org/

## Getting Help

If you encounter issues:
1. Check this guide carefully
2. Review error messages
3. Check Django/MySQL logs
4. Verify all prerequisites are installed
5. Ensure MySQL is running
6. Check firewall settings

---

Good luck with your MediGenAI installation! 🏥✨
