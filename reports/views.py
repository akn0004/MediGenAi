from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from .models import Patient, MedicalReport
from .forms import PatientForm, MedicalReportForm
import random

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    total_patients = Patient.objects.count()
    total_reports = MedicalReport.objects.count()
    pending_requests = MedicalReport.objects.filter(status='at_risk').count()
    ai_generated = MedicalReport.objects.filter(ai_generated=True).count()
    
    # Recent patients with their latest report
    recent_reports = MedicalReport.objects.select_related('patient').order_by('-date_created')[:5]
    
    # AI Analysis data
    status_counts = MedicalReport.objects.values('status').annotate(count=Count('id'))
    analysis_data = {
        'normal': 0,
        'at_risk': 0,
        'critical': 0
    }
    for item in status_counts:
        if item['status'] in analysis_data:
            analysis_data[item['status']] = item['count']
    
    context = {
        'total_patients': total_patients,
        'total_reports': total_reports,
        'pending_requests': pending_requests,
        'ai_generated': ai_generated,
        'recent_reports': recent_reports,
        'analysis_data': analysis_data,
    }
    return render(request, 'dashboard.html', context)

@login_required
def patients_view(request):
    patients = Patient.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        patients = patients.filter(
            Q(name__icontains=search_query) | 
            Q(contact_number__icontains=search_query)
        )
    
    context = {
        'patients': patients,
        'search_query': search_query,
    }
    return render(request, 'patients.html', context)

@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            
            # Create a report for the patient
            report = MedicalReport.objects.create(
                patient=patient,
                status=random.choice(['normal', 'at_risk', 'critical']),
                ai_generated=True,
                created_by=request.user,
                content=f"Medical report for {patient.name}",
                diagnosis="AI-generated preliminary diagnosis",
                recommendations="Follow-up recommended"
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Patient added successfully!'
                })
            
            messages.success(request, 'Patient added successfully!')
            return redirect('dashboard')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def reports_view(request):
    reports = MedicalReport.objects.select_related('patient').all()
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        reports = reports.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        reports = reports.filter(
            Q(report_id__icontains=search_query) | 
            Q(patient__name__icontains=search_query)
        )
    
    context = {
        'reports': reports,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'reports.html', context)

@login_required
def report_detail(request, report_id):
    report = get_object_or_404(MedicalReport, report_id=report_id)
    context = {
        'report': report,
    }
    return render(request, 'report_detail.html', context)

@login_required
def ai_analysis_view(request):
    # Get all reports with analysis
    reports = MedicalReport.objects.select_related('patient').filter(ai_generated=True)
    
    # Status distribution
    status_counts = MedicalReport.objects.values('status').annotate(count=Count('id'))
    analysis_data = {
        'normal': 0,
        'at_risk': 0,
        'critical': 0
    }
    for item in status_counts:
        if item['status'] in analysis_data:
            analysis_data[item['status']] = item['count']
    
    context = {
        'reports': reports,
        'analysis_data': analysis_data,
    }
    return render(request, 'ai_analysis.html', context)
