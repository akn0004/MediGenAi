from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patients/', views.patients_view, name='patients'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('edit-patient/', views.edit_patient, name='edit_patient'),
    path('reports/', views.reports_view, name='reports'),
    path('add-report/', views.add_report, name='add_report'),
    path('reports/<str:report_id>/', views.report_detail, name='report_detail'),
    path('ai-analysis/', views.ai_analysis_view, name='ai_analysis'),
    path('tests/', views.tests_view, name='tests'),
    path('add-test/', views.add_test, name='add_test'),
    path('get-test-group/', views.get_test_group, name='get_test_group'),
    path('update-test-group/', views.update_test_group, name='update_test_group'),
    path('update-test/', views.update_test, name='update_test'),
    path('publish-tests/', views.publish_tests, name='publish_tests'),
    path('delete-test/', views.delete_test, name='delete_test'),
    path('bulk-delete-tests/', views.bulk_delete_tests, name='bulk_delete_tests'),
    path('delete-report/<str:report_id>/', views.delete_report, name='delete_report'),
    path('bulk-delete-reports/', views.bulk_delete_reports, name='bulk_delete_reports'),
    path('delete-patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('bulk-delete-patients/', views.bulk_delete_patients, name='bulk_delete_patients'),
    path('generate-ai-report/<str:report_id>/', views.generate_ai_report, name='generate_ai_report'),
    path('settings/', views.settings_view, name='settings'),
    
    # Patient Portal URLs
    path('patient/logout/', views.patient_logout_view, name='patient_logout'),
    path('patient/portal/', views.patient_portal, name='patient_portal'),
    path('patient/reports/<str:report_id>/', views.patient_report_detail, name='patient_report_detail'),
]
