from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='patient_profile')
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100, blank=True, null=True)  # Store plain text password for patient access
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


class TestCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Test Categories'


class TestType(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, related_name='test_types')
    unit = models.CharField(max_length=50, blank=True, null=True)
    normal_range_min = models.FloatField(blank=True, null=True)
    normal_range_max = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"
    
    class Meta:
        ordering = ['category', 'name']


class PatientTest(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal'),
        ('critical', 'Critical'),
    ]
    
    test_id = models.CharField(max_length=20, unique=True)
    test_group = models.CharField(max_length=20, default='SINGLE')  # Groups multiple test types together
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='tests')
    report = models.ForeignKey('MedicalReport', on_delete=models.CASCADE, related_name='tests', null=True, blank=True)
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    test_date = models.DateTimeField(default=timezone.now)
    result_value = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal')
    notes = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.test_id} - {self.patient.name} - {self.test_type.name}"
    
    def save(self, *args, **kwargs):
        if not self.test_id:
            # Auto-generate test ID
            last_test = PatientTest.objects.all().order_by('id').last()
            if last_test:
                last_num = int(last_test.test_id.split('-')[1])
                self.test_id = f'TEST-{str(last_num + 1).zfill(4)}'
            else:
                self.test_id = 'TEST-0001'
        
        # Auto-determine status based on normal range
        if self.test_type.normal_range_min and self.test_type.normal_range_max:
            if self.result_value < self.test_type.normal_range_min or self.result_value > self.test_type.normal_range_max:
                if self.result_value < self.test_type.normal_range_min * 0.5 or self.result_value > self.test_type.normal_range_max * 1.5:
                    self.status = 'critical'
                else:
                    self.status = 'abnormal'
            else:
                self.status = 'normal'
        
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-test_date']


class LabSettings(models.Model):
    lab_name = models.CharField(max_length=200, default='MediGen Laboratory')
    lab_address = models.TextField(default='123 Medical Center Drive, Healthcare City')
    lab_phone = models.CharField(max_length=50, blank=True, null=True)
    lab_email = models.EmailField(blank=True, null=True)
    lab_logo = models.ImageField(upload_to='lab_logos/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.lab_name
    
    class Meta:
        verbose_name = 'Lab Settings'
        verbose_name_plural = 'Lab Settings'
    
    @classmethod
    def get_settings(cls):
        """Get or create singleton settings instance"""
        settings, created = cls.objects.get_or_create(id=1)
        return settings
