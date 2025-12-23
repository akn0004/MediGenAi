# Logo Setup Instructions

## Step 1: Save the Logo Image

Please save the MediGenAI logo image you provided as:

**File name:** `logo.png`  
**Location:** `c:\Users\ecbin\Workspace\MediGenAi\static\images\logo.png`

### Instructions:
1. Right-click on the logo image you have
2. Select "Save As" or "Save Image As"
3. Navigate to `c:\Users\ecbin\Workspace\MediGenAi\static\images\`
4. Name it exactly as: `logo.png`
5. Click Save

## Step 2: Verify the Logo is Updated

After saving the logo file, restart your Django development server:

```bash
python manage.py runserver
```

Or if using the provided scripts:
```bash
.\run.ps1
```

## What Has Been Updated

The following templates have been updated to use the new logo:

1. **base.html** - Main navigation sidebar logo (used by all authenticated pages)
   - Dashboard
   - Reports
   - Patients
   - AI Analysis
   - Report Details

2. **login.html** - Login page logo

## Logo Specifications

- **Format:** PNG (with transparent background recommended)
- **Size:** The logo will be displayed at:
  - 50x50 pixels in the sidebar
  - 80x80 pixels on the login page
- **Original size:** Ideally 200x200 pixels or higher for best quality

## If You Need to Use a Different Image Format

If you have the logo in a different format (e.g., `.jpg`, `.svg`), update the file references:

In **base.html** line ~192:
```html
<img src="{% static 'images/logo.svg' %}" alt="MediGenAI Logo">
```

In **login.html** line ~220:
```html
<img src="{% static 'images/logo.svg' %}" alt="MediGenAI Logo">
```
