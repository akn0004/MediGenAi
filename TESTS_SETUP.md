# Instructions to Set Up Tests Feature

## Step 1: Stop the Django server
Press `CTRL+BREAK` or `CTRL+C` in the terminal running the server

## Step 2: Run migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

## Step 3: Populate test categories and types
```powershell
python manage.py populate_tests
```

## Step 4: Start the server again
```powershell
python manage.py runserver
```

## Step 5: Access the Tests tab
Navigate to: http://localhost:8000/tests/

---

## What's New

### Tests Tab Features:
1. **Test Categories**: Tests are organized into groups:
   - Blood Count (Hemoglobin, WBC, Platelets, RBC)
   - Vitamins (Vitamin D, B12, Folate)
   - Minerals (Iron, Calcium, Magnesium)
   - Lipid Panel (Cholesterol, LDL, HDL, Triglycerides)
   - Glucose Tests (Fasting Glucose, HbA1c, Random Glucose)
   - Liver Function (ALT, AST, Alkaline Phosphatase, Bilirubin)
   - Kidney Function (Creatinine, BUN, eGFR)
   - Thyroid Function (TSH, Free T4, Free T3)
   - Vital Signs (Blood Pressure, Heart Rate, Temperature)

2. **Add New Tests**: 
   - Select a patient
   - Choose a test type from the categorized list
   - Enter the result value
   - System automatically shows units and normal ranges
   - Status (Normal/Abnormal/Critical) is auto-calculated

3. **View All Tests**: Tabular display showing:
   - Test ID
   - Patient name
   - Test type and category
   - Result value with units
   - Normal range
   - Test date
   - Status badge (color-coded)

4. **Statistics**: 4 stat cards showing:
   - Total Tests
   - Normal Tests
   - Abnormal Tests
   - Critical Tests

## Database Models Added:
- `TestCategory`: Groups of related tests
- `TestType`: Individual test types with units and normal ranges
- `PatientTest`: Test results for patients with auto-status calculation
