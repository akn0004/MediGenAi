# Management command to populate sample data
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reports.models import Patient, MedicalReport
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@medigenai.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created: admin/admin123'))

        # Sample patient names
        patient_names = [
            ('John Doe', 45, 'male', '1234567890'),
            ('Sarah Smith', 34, 'female', '1234567891'),
            ('Robert Brown', 52, 'male', '1234567892'),
            ('Emily White', 28, 'female', '1234567893'),
            ('Michael Green', 61, 'male', '1234567894'),
            ('Jessica Lee', 39, 'female', '1234567895'),
            ('David Wilson', 47, 'male', '1234567896'),
            ('Lisa Anderson', 33, 'female', '1234567897'),
            ('James Taylor', 55, 'male', '1234567898'),
            ('Maria Garcia', 42, 'female', '1234567899'),
        ]

        statuses = ['normal', 'at_risk', 'critical']
        admin_user = User.objects.get(username='admin')

        # Create patients and reports
        for name, age, gender, contact in patient_names:
            if not Patient.objects.filter(name=name).exists():
                patient = Patient.objects.create(
                    name=name,
                    age=age,
                    gender=gender,
                    contact_number=contact
                )

                # Create 1-3 reports per patient
                num_reports = random.randint(1, 3)
                for i in range(num_reports):
                    status = random.choice(statuses)
                    days_ago = random.randint(1, 30)
                    
                    MedicalReport.objects.create(
                        patient=patient,
                        date_created=timezone.now() - timedelta(days=days_ago),
                        status=status,
                        ai_generated=True,
                        content=f"Medical examination report for {name}. Patient presented with routine checkup.",
                        diagnosis=f"{'Normal health indicators' if status == 'normal' else 'Requires attention and monitoring' if status == 'at_risk' else 'Immediate medical intervention required'}",
                        recommendations=f"{'Continue regular health maintenance' if status == 'normal' else 'Follow-up appointment recommended within 2 weeks' if status == 'at_risk' else 'Emergency consultation required'}",
                        created_by=admin_user
                    )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {Patient.objects.count()} patients'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {MedicalReport.objects.count()} reports'))
