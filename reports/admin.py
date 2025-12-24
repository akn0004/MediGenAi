from django.contrib import admin
from .models import Patient, MedicalReport, TestCategory, TestType, PatientTest, LabSettings

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


@admin.register(LabSettings)
class LabSettingsAdmin(admin.ModelAdmin):
    list_display = ('lab_name', 'lab_phone', 'lab_email', 'updated_at', 'updated_by')
    readonly_fields = ('updated_at', 'updated_by')
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not LabSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of settings
        return False
