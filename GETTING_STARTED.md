# 🚀 Getting Started with MediGenAI

## Welcome!

This guide will help you get MediGenAI running on your computer in just a few minutes.

---

## ✅ Pre-Installation Checklist

Before starting, make sure you have:

- [ ] **Windows 10/11** (or Linux/macOS)
- [ ] **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- [ ] **MySQL 8.0+** installed ([Download](https://dev.mysql.com/downloads/installer/))
- [ ] **Internet connection** (for downloading packages)
- [ ] **At least 500MB free disk space**

---

## 🎯 Installation Methods

Choose the method that works best for you:

### Method 1: Automated Setup (⭐ Recommended for Beginners)

**For Windows PowerShell:**
```powershell
# 1. Open PowerShell in the MediGenAi folder
# 2. Run:
.\setup.ps1
```

**For Windows Command Prompt:**
```cmd
# 1. Open CMD in the MediGenAi folder
# 2. Run:
setup.bat
```

The script will automatically:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Set up configuration
- ✅ Create database tables
- ✅ Add sample data

**That's it! Skip to "First Login" section below.**

---

### Method 2: Manual Setup (For Advanced Users)

If automated setup doesn't work, follow these steps:

#### Step 1: Create MySQL Database

Open MySQL and create the database:
```sql
CREATE DATABASE medigenai_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# OR activate it (Windows CMD)
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Configure Environment

```bash
# Copy environment file
copy .env.example .env

# Edit .env file and set:
# DB_PASSWORD=your_mysql_password
```

#### Step 4: Initialize Database

```bash
# Create database tables
python manage.py migrate

# Load sample data
python manage.py populate_data
```

---

## 🎬 Running the Application

### Starting the Server

**Quick Way:**
```bash
# Windows PowerShell
.\run.ps1

# Windows CMD
run.bat
```

**Manual Way:**
```bash
# Activate environment
.\venv\Scripts\Activate.ps1

# Start server
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Accessing the Application

Open your web browser and go to:
```
http://localhost:8000
```

---

## 🔐 First Login

Use these credentials to log in:

```
Username: admin
Password: admin123
```

> **Security Note**: Change this password after first login in production!

---

## 🎓 Quick Tour

### 1. Dashboard (Home Page)
After login, you'll see:
- **Statistics**: Total patients, reports, pending requests
- **Add Patient Form**: Quick way to add new patients
- **Recent Patients**: Latest reports in a table
- **AI Analysis**: Overview of status distribution

**Try This**: Add a new patient using the form!

### 2. Patients Page
Click "Patients" in the sidebar to see:
- All patients in a grid layout
- Search functionality
- Patient details (age, gender, contact)

**Try This**: Use the search bar to find "John"!

### 3. Reports Page
Click "Reports" in the sidebar to see:
- All medical reports in a table
- Filter by status (Normal, At Risk, Critical)
- Search by report ID or patient name
- AI-generated indicators

**Try This**: Filter reports by "At Risk" status!

### 4. Report Detail
Click "View" on any report to see:
- Complete patient information
- Report content and diagnosis
- Recommendations
- Print functionality

**Try This**: Click print to see the print preview!

### 5. AI Analysis
Click "AI Analysis" in the sidebar to see:
- Visual chart of status distribution
- Statistics overview
- List of AI-generated reports

**Try This**: Explore the different sections!

---

## 📊 Understanding Sample Data

The system comes with sample data:

### Sample Patients (10 total)
- John Doe, Sarah Smith, Robert Brown, Emily White
- Michael Green, Jessica Lee, David Wilson
- Lisa Anderson, James Taylor, Maria Garcia

### Sample Reports
- Report IDs: REP-001 through REP-067
- Different statuses: Normal, At Risk, Critical
- AI-generated content
- Dates from the last 30 days

---

## 🎯 Common Tasks

### Adding a New Patient

1. Go to Dashboard
2. Fill in the "Add New Patient" form:
   - Name
   - Age
   - Gender
   - Contact Number
3. Click "Add Patient"
4. Success message will appear
5. Page will refresh with new data

### Viewing a Report

1. Go to Reports page
2. Find the report you want
3. Click the "View" button
4. See all report details
5. Use "Print" if needed

### Searching for Data

**Search Patients:**
1. Go to Patients page
2. Use search bar at top
3. Type name or contact number
4. Press Enter or click Search

**Search Reports:**
1. Go to Reports page
2. Use search bar
3. Type Report ID or patient name
4. Click Filter button

### Filtering Reports

1. Go to Reports page
2. Use the Status dropdown
3. Select: All, Normal, At Risk, or Critical
4. Click Filter
5. See filtered results

---

## 🔧 Admin Panel Access

Django includes a powerful admin panel:

### Accessing Admin Panel

1. Go to: `http://localhost:8000/admin`
2. Login with: admin / admin123
3. You can:
   - View all data
   - Edit records
   - Delete records
   - Add new users

---

## 💡 Tips & Tricks

### Keyboard Shortcuts
- **Ctrl + C**: Stop the server
- **F5**: Refresh the page
- **Ctrl + P**: Print report (on detail page)

### Navigation Tips
- Use sidebar for main navigation
- Click logo to return to Dashboard
- Use "Back" buttons to navigate
- Browser back button works too

### Performance Tips
- Keep MySQL service running
- Don't close terminal while server is running
- Use Chrome/Firefox for best experience
- Clear browser cache if styles look broken

---

## 🐛 Troubleshooting

### Server Won't Start

**Problem**: "Port 8000 already in use"
**Solution**: 
```bash
# Use different port
python manage.py runserver 8080
# Then access: http://localhost:8080
```

**Problem**: "Can't find manage.py"
**Solution**: Make sure you're in the MediGenAi folder

### Can't Login

**Problem**: Invalid credentials
**Solution**: 
```bash
# Create new superuser
python manage.py createsuperuser
```

### Page Looks Broken

**Problem**: CSS not loading
**Solution**:
1. Hard refresh: Ctrl + F5
2. Clear browser cache
3. Check if server is running

### Database Errors

**Problem**: "No such table"
**Solution**:
```bash
# Run migrations
python manage.py migrate
```

**Problem**: "Can't connect to MySQL"
**Solution**:
1. Check if MySQL is running
2. Verify password in .env file
3. Check MySQL service status

---

## 🎓 Next Steps

### For Learning:
1. Explore all pages thoroughly
2. Try adding multiple patients
3. View different reports
4. Check AI analysis charts
5. Try the admin panel

### For Development:
1. Read Django documentation
2. Understand the models in `reports/models.py`
3. Explore views in `reports/views.py`
4. Customize templates in `templates/`
5. Add your own features

### For Production:
1. Change DEBUG to False
2. Set strong SECRET_KEY
3. Update ALLOWED_HOSTS
4. Use production database
5. Set up proper hosting
6. Configure HTTPS

---

## 📚 Documentation Files

Refer to these for more information:

- **README.md** - Main documentation
- **QUICKSTART.md** - Quick setup guide
- **INSTALLATION.md** - Detailed installation
- **PROJECT_SUMMARY.md** - Project overview
- **PAGE_LAYOUTS.md** - Visual page guide

---

## 🆘 Getting Help

### Error Messages
- Read the error message carefully
- Check the terminal output
- Look for red error text

### Documentation
- Check the documentation files
- Read Django docs: https://docs.djangoproject.com/
- MySQL docs: https://dev.mysql.com/doc/

### Common Issues
Most issues are related to:
1. MySQL not running
2. Wrong credentials
3. Missing migrations
4. Virtual environment not activated

---

## ✨ Features to Explore

- [ ] Add a new patient
- [ ] View patient details
- [ ] Filter reports by status
- [ ] View AI analysis charts
- [ ] Try the search functionality
- [ ] Print a report
- [ ] Access admin panel
- [ ] Create a new user

---

## 🎉 You're Ready!

Congratulations! You now have a fully functional MediGenAI application.

**Remember:**
- Keep MySQL running
- Activate virtual environment before running
- Use the documentation when stuck
- Explore and experiment!

**Quick Commands:**
```bash
# Start server
.\run.ps1          # or run.bat

# Stop server
Ctrl + C

# Access application
http://localhost:8000

# Login
admin / admin123
```

---

**Enjoy using MediGenAI! 🏥✨**

If you have questions, refer to the documentation files or explore the Django and MySQL documentation online.
