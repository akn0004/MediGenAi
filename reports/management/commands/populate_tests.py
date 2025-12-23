from django.core.management.base import BaseCommand
from reports.models import TestCategory, TestType

class Command(BaseCommand):
    help = 'Populate test categories and test types'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating test categories and types...')

        # Define test categories and their tests
        test_data = {
            'Blood Count': [
                {'name': 'Hemoglobin', 'unit': 'g/dL', 'min': 13.5, 'max': 17.5},
                {'name': 'White Blood Cell Count', 'unit': '10^3/μL', 'min': 4.5, 'max': 11.0},
                {'name': 'Platelet Count', 'unit': '10^3/μL', 'min': 150, 'max': 400},
                {'name': 'Red Blood Cell Count', 'unit': '10^6/μL', 'min': 4.5, 'max': 5.5},
            ],
            'Vitamins': [
                {'name': 'Vitamin D', 'unit': 'ng/mL', 'min': 30, 'max': 100},
                {'name': 'Vitamin B12', 'unit': 'pg/mL', 'min': 200, 'max': 900},
                {'name': 'Folate', 'unit': 'ng/mL', 'min': 2.7, 'max': 17.0},
            ],
            'Minerals': [
                {'name': 'Iron', 'unit': 'μg/dL', 'min': 60, 'max': 170},
                {'name': 'Calcium', 'unit': 'mg/dL', 'min': 8.5, 'max': 10.5},
                {'name': 'Magnesium', 'unit': 'mg/dL', 'min': 1.7, 'max': 2.2},
            ],
            'Lipid Panel': [
                {'name': 'Total Cholesterol', 'unit': 'mg/dL', 'min': 0, 'max': 200},
                {'name': 'LDL Cholesterol', 'unit': 'mg/dL', 'min': 0, 'max': 100},
                {'name': 'HDL Cholesterol', 'unit': 'mg/dL', 'min': 40, 'max': 60},
                {'name': 'Triglycerides', 'unit': 'mg/dL', 'min': 0, 'max': 150},
            ],
            'Glucose Tests': [
                {'name': 'Fasting Glucose', 'unit': 'mg/dL', 'min': 70, 'max': 100},
                {'name': 'HbA1c', 'unit': '%', 'min': 4.0, 'max': 5.6},
                {'name': 'Random Glucose', 'unit': 'mg/dL', 'min': 70, 'max': 140},
            ],
            'Liver Function': [
                {'name': 'ALT (SGPT)', 'unit': 'U/L', 'min': 7, 'max': 56},
                {'name': 'AST (SGOT)', 'unit': 'U/L', 'min': 10, 'max': 40},
                {'name': 'Alkaline Phosphatase', 'unit': 'U/L', 'min': 44, 'max': 147},
                {'name': 'Bilirubin Total', 'unit': 'mg/dL', 'min': 0.1, 'max': 1.2},
            ],
            'Kidney Function': [
                {'name': 'Creatinine', 'unit': 'mg/dL', 'min': 0.7, 'max': 1.3},
                {'name': 'BUN', 'unit': 'mg/dL', 'min': 7, 'max': 20},
                {'name': 'eGFR', 'unit': 'mL/min/1.73m²', 'min': 60, 'max': 120},
            ],
            'Thyroid Function': [
                {'name': 'TSH', 'unit': 'μIU/mL', 'min': 0.4, 'max': 4.0},
                {'name': 'Free T4', 'unit': 'ng/dL', 'min': 0.8, 'max': 1.8},
                {'name': 'Free T3', 'unit': 'pg/mL', 'min': 2.3, 'max': 4.2},
            ],
            'Vital Signs': [
                {'name': 'Systolic Blood Pressure', 'unit': 'mmHg', 'min': 90, 'max': 120},
                {'name': 'Diastolic Blood Pressure', 'unit': 'mmHg', 'min': 60, 'max': 80},
                {'name': 'Heart Rate', 'unit': 'bpm', 'min': 60, 'max': 100},
                {'name': 'Body Temperature', 'unit': '°F', 'min': 97.0, 'max': 99.0},
            ],
        }

        created_count = 0
        for category_name, tests in test_data.items():
            category, created = TestCategory.objects.get_or_create(
                name=category_name,
                defaults={'description': f'{category_name} tests'}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category_name}'))

            for test in tests:
                test_type, created = TestType.objects.get_or_create(
                    name=test['name'],
                    category=category,
                    defaults={
                        'unit': test['unit'],
                        'normal_range_min': test['min'],
                        'normal_range_max': test['max']
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'  - Created test: {test["name"]}')

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} test types!'))
