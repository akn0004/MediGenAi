from django.contrib import admin
from .models import Patient, MedicalReport, TestCategory, TestType, PatientTest

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

@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(TestType)
class TestTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit', 'normal_range_min', 'normal_range_max')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

@admin.register(PatientTest)
class PatientTestAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'patient', 'test_type', 'result_value', 'status', 'test_date')
    search_fields = ('test_id', 'patient__name', 'test_type__name')
    list_filter = ('status', 'test_date', 'test_type__category')

