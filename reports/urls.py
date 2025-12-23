from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patients/', views.patients_view, name='patients'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('reports/', views.reports_view, name='reports'),
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
]
