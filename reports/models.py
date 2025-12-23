from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

class MedicalReport(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('at_risk', 'At Risk'),
        ('critical', 'Critical'),
    ]
    
    report_id = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reports')
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal')
    ai_generated = models.BooleanField(default=False)
    content = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.report_id} - {self.patient.name}"
    
    def save(self, *args, **kwargs):
        if not self.report_id:
            # Auto-generate report ID
            last_report = MedicalReport.objects.all().order_by('id').last()
            if last_report:
                last_num = int(last_report.report_id.split('-')[1])
                self.report_id = f'REP-{str(last_num + 1).zfill(3)}'
            else:
                self.report_id = 'REP-001'
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-date_created']
