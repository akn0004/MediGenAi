# Quick Start Guide for MediGenAI

## Prerequisites Checklist
- [ ] Python 3.8 or higher installed
- [ ] MySQL 8.0 or higher installed and running
- [ ] Git (optional, for version control)

## Installation Steps

### 1. Database Setup (IMPORTANT - Do this first!)

Open MySQL Command Line or MySQL Workbench and run:

```sql
CREATE DATABASE medigenai_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Verify the database was created:
```sql
SHOW DATABASES;
```

### 2. Automated Setup (Easiest Method)

#### For PowerShell users:
```powershell
.\setup.ps1
```

#### For Command Prompt users:
```cmd
setup.bat
```

The script will:
- Create virtual environment
- Install all Python packages
- Create .env configuration file
- Run database migrations
- Create sample data
- Set up admin account

### 3. Manual Setup (Alternative)

If automated setup doesn't work, follow these steps:

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

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Configure Environment**

Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

Edit `.env` and update these values:
```
DB_NAME=medigenai_db
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD_HERE
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your-secret-key-change-this
DEBUG=True
```

**Step 5: Database Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Step 6: Create Sample Data**
```bash
python manage.py populate_data
```

**Step 7: Run Development Server**
```bash
python manage.py runserver
```

### 4. Access the Application

Open your web browser and go to:
```
http://localhost:8000
```

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

## What You'll See

After logging in, you'll have access to:

1. **Dashboard** - Overview with statistics and quick actions
2. **Patients** - List of all patients with their information
3. **Reports** - Medical reports with different statuses
4. **AI Analysis** - Visual analytics and AI-generated insights

## Sample Data Included

The system comes pre-populated with:
- 10 sample patients (John Doe, Sarah Smith, etc.)
- Multiple medical reports per patient
- Different status types (Normal, At Risk, Critical)
- AI-generated analysis data

## Troubleshooting

### Problem: "Can't connect to MySQL server"
**Solution:**
1. Make sure MySQL service is running
2. Check if port 3306 is open
3. Verify credentials in `.env` file

### Problem: "mysqlclient failed to install"
**Solution:**
1. Install Microsoft Visual C++ Build Tools
2. Or download pre-built wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

### Problem: "Module not found" error
**Solution:**
1. Make sure virtual environment is activated
2. Run: `pip install -r requirements.txt` again

### Problem: "Port 8000 already in use"
**Solution:**
Run on a different port:
```bash
python manage.py runserver 8080
```

### Problem: Can't login
**Solution:**
Create a new superuser:
```bash
python manage.py createsuperuser
```

## Next Steps

1. Explore the dashboard and different sections
2. Try adding a new patient
3. View generated reports
4. Check the AI analysis page
5. Customize the application as needed

## Need Help?

- Check the main README.md for detailed documentation
- Review Django documentation: https://docs.djangoproject.com/
- Check MySQL connection settings in medigenai/settings.py

---

Enjoy using MediGenAI! 🏥🤖
