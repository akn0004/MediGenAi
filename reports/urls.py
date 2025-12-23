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
]
