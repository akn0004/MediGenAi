# MediGenAI - AI-Assisted Medical Report Generation System

A comprehensive web application for managing medical reports with AI-powered analysis. Built with Django, HTML, CSS, JavaScript, and MySQL.

## Features

- 🔐 **Secure Authentication** - Login system with user management
- 📊 **Dashboard** - Real-time overview of patients, reports, and analytics
- 👥 **Patient Management** - Add, view, and manage patient records
- 📝 **Medical Reports** - Generate and manage medical reports
- 🤖 **AI Analysis** - AI-powered report generation and analysis
- 📈 **Analytics** - Visual insights into patient status distribution
- 🎨 **Modern UI** - Beautiful gradient-based design with responsive layout

## Technology Stack

- **Backend**: Python Django 4.2.7
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, jQuery
- **Icons**: Font Awesome 6.4.0

## Quick Setup (Automated)

### Option 1: Using PowerShell (Recommended for Windows)
```powershell
.\setup.ps1
```

### Option 2: Using Batch File
```cmd
setup.bat
```

The automated setup will:
- Create a virtual environment
- Install all dependencies
- Set up environment variables
- Run database migrations
- Create sample data with 10 patients and multiple reports
- Create an admin user (username: admin, password: admin123)

## Manual Setup

### Prerequisites

1. **Python 3.8+** installed
2. **MySQL 8.0+** installed and running
3. **pip** package manager

### Step-by-Step Instructions

1. **Clone or navigate to the project directory**
```bash
cd MediGenAi
```

2. **Create and activate virtual environment**
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1

# Activate on Windows CMD
venv\Scripts\activate.bat
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create MySQL database**

Open MySQL and run:
```sql
CREATE DATABASE medigenai_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. **Configure environment variables**
```bash
# Copy the example env file
copy .env.example .env

# Edit .env file and update with your MySQL credentials:
# DB_NAME=medigenai_db
# DB_USER=root
# DB_PASSWORD=your_mysql_password
# DB_HOST=localhost
# DB_PORT=3306
```

6. **Run database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create sample data (optional but recommended)**
```bash
python manage.py populate_data
```

This creates:
- Admin user (username: admin, password: admin123)
- 10 sample patients
- Multiple medical reports with different statuses

8. **Start the development server**
```bash
python manage.py runserver
```

9. **Access the application**

Open your browser and navigate to: **http://localhost:8000**

## Default Login Credentials

After running `populate_data`:
- **Username**: admin
- **Password**: admin123

## Application Structure

```
MediGenAi/
├── medigenai/              # Project settings
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL configuration
│   └── wsgi.py            # WSGI configuration
├── reports/               # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Form definitions
│   ├── urls.py            # App URLs
│   └── management/        # Custom commands
│       └── commands/
│           └── populate_data.py
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── dashboard.html     # Dashboard
│   ├── patients.html      # Patients list
│   ├── reports.html       # Reports list
│   ├── report_detail.html # Report details
│   └── ai_analysis.html   # AI analysis
├── static/                # Static files (CSS, JS, images)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Database Models

### Patient
- Name, age, gender, contact number
- Timestamps for creation and updates

### MedicalReport
- Auto-generated report ID (REP-001, REP-002, etc.)
- Patient reference
- Status (Normal, At Risk, Critical)
- AI-generated flag
- Content, diagnosis, recommendations
- Created by user reference

## Features Overview

### 1. Login Page
- Secure authentication
- Modern gradient design
- Form validation

### 2. Dashboard
- Statistics cards (Total Patients, Reports, Pending Requests, AI-Generated)
- Add new patient form
- Recent patients table
- AI analysis overview chart

### 3. Patients Page
- Grid view of all patients
- Search functionality
- Patient details (age, gender, contact, reports count)

### 4. Reports Page
- Table view of all reports
- Filter by status
- Search by report ID or patient name
- AI-generated indicator

### 5. Report Detail Page
- Complete report information
- Patient details
- Diagnosis and recommendations
- Print functionality

### 6. AI Analysis Page
- Status distribution chart
- Statistics overview
- List of AI-generated reports
- Visual analytics

## Common Issues & Solutions

### MySQL Connection Error
```
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```
**Solution**: Make sure MySQL is running and credentials in `.env` are correct

### mysqlclient Installation Error
```
error: Microsoft Visual C++ 14.0 or greater is required
```
**Solution**: 
- Install Microsoft C++ Build Tools
- Or use: `pip install mysqlclient-1.4.6-cp39-cp39-win_amd64.whl` (download appropriate wheel)

### Port Already in Use
```
Error: That port is already in use.
```
**Solution**: Use a different port: `python manage.py runserver 8080`

## Development

### Creating a Superuser Manually
```bash
python manage.py createsuperuser
```

### Running Tests
```bash
python manage.py test
```

### Clearing Database and Starting Fresh
```bash
python manage.py flush
python manage.py populate_data
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` in `settings.py`
3. Set a strong `SECRET_KEY`
4. Use a production-grade database
5. Configure static files serving
6. Use a production server (Gunicorn, uWSGI)
7. Set up HTTPS

## License

This project is for educational purposes.

## Support

For issues or questions, please check the setup instructions or review the code comments.

---

**Made with ❤️ for better healthcare management**
