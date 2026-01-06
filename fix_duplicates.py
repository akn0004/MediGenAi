"""
Script to fix duplicate contact numbers in the Patient table
"""
import os
import django
import sys

# Add the project directory to the path
sys.path.append('c:/Users/ecbin/Workspace/MediGenAi')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medigenai.settings')
django.setup()

from reports.models import Patient
from collections import defaultdict
import random

def fix_duplicates():
    # Find all contact numbers that have duplicates
    contact_map = defaultdict(list)
    
    for patient in Patient.objects.all():
        contact_map[patient.contact_number].append(patient)
    
    # Fix duplicates by appending random digits
    fixed_count = 0
    for contact_number, patients in contact_map.items():
        if len(patients) > 1:
            print(f"Found {len(patients)} duplicates for contact: {contact_number}")
            # Keep the first one, modify the rest
            for i, patient in enumerate(patients[1:], 1):
                # Generate a unique contact number
                base_number = contact_number[:7] if len(contact_number) >= 7 else contact_number
                new_number = base_number + str(random.randint(100, 999))
                
                # Ensure uniqueness
                attempts = 0
                while Patient.objects.filter(contact_number=new_number).exists() and attempts < 100:
                    new_number = base_number + str(random.randint(100, 999))
                    attempts += 1
                
                print(f"  Changing {patient.name}'s contact from {contact_number} to {new_number}")
                patient.contact_number = new_number
                patient.save()
                fixed_count += 1
    
    print(f"\nFixed {fixed_count} duplicate contact numbers")
    return fixed_count

if __name__ == '__main__':
    fix_duplicates()
