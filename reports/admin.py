from django.contrib import admin
from .models import Patient, MedicalReport

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'contact_number', 'created_at')
    search_fields = ('name', 'contact_number')
    list_filter = ('gender', 'created_at')

@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'patient', 'status', 'date_created', 'ai_generated')
    search_fields = ('report_id', 'patient__name')
    list_filter = ('status', 'ai_generated', 'date_created')
