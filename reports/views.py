from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone
from .models import Patient, MedicalReport, TestCategory, TestType, PatientTest
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
    
    # Get published test groups for this patient
    from collections import defaultdict
    all_tests = PatientTest.objects.filter(
        patient=report.patient,
        is_published=True
    ).select_related('test_type', 'test_type__category').order_by('-test_date', 'test_group')
    
    # Group tests by test_group
    test_groups = defaultdict(list)
    for test in all_tests:
        test_groups[test.test_group].append(test)
    
    context = {
        'report': report,
        'test_groups': list(test_groups.values()),
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


@login_required
def tests_view(request):
    # Get all test categories with their test types
    categories = TestCategory.objects.prefetch_related('test_types').all()
    
    # Get all patients for the dropdown
    patients = Patient.objects.all()
    
    # Get all patient tests grouped by test_group
    all_tests = PatientTest.objects.select_related('patient', 'test_type', 'test_type__category').order_by('-test_date', 'test_group')
    
    # Group tests by test_group
    from collections import defaultdict
    draft_groups = defaultdict(list)
    published_groups = defaultdict(list)
    
    for test in all_tests:
        if test.is_published:
            published_groups[test.test_group].append(test)
        else:
            draft_groups[test.test_group].append(test)
    
    # Convert to list of groups (each group is a list of tests)
    draft_test_groups = list(draft_groups.values())
    published_test_groups = list(published_groups.values())
    
    # Test statistics
    total_tests = len(draft_groups) + len(published_groups)  # Count test groups, not individual tests
    draft_count = len(draft_groups)
    published_count = len(published_groups)
    
    # Count status from published tests
    published_tests = PatientTest.objects.filter(is_published=True)
    abnormal_tests = published_tests.filter(status='abnormal').values('test_group').distinct().count()
    critical_tests = published_tests.filter(status='critical').values('test_group').distinct().count()
    
    context = {
        'categories': categories,
        'patients': patients,
        'draft_test_groups': draft_test_groups,
        'published_test_groups': published_test_groups,
        'total_tests': total_tests,
        'draft_count': draft_count,
        'published_count': published_count,
        'abnormal_tests': abnormal_tests,
        'critical_tests': critical_tests,
    }
    return render(request, 'tests.html', context)


@login_required
def add_test(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        test_type_ids = request.POST.getlist('test_type_ids[]')
        result_value = request.POST.get('result_value', 0)
        
        try:
            patient = Patient.objects.get(id=patient_id)
            
            # Generate a unique test group ID for this batch of tests
            last_test = PatientTest.objects.all().order_by('id').last()
            if last_test:
                last_num = int(last_test.test_id.split('-')[1])
                test_group = f'GRP-{str(last_num + 1).zfill(4)}'
            else:
                test_group = 'GRP-0001'
            
            created_tests = []
            for test_type_id in test_type_ids:
                test_type = TestType.objects.get(id=test_type_id)
                
                test = PatientTest.objects.create(
                    patient=patient,
                    test_type=test_type,
                    test_group=test_group,  # Assign same group ID
                    result_value=float(result_value),
                    is_published=False,
                    created_by=request.user
                )
                created_tests.append(test.test_id)
            
            messages.success(request, f'Test group created with {len(created_tests)} test type(s)!')
            return JsonResponse({'success': True, 'test_group': test_group, 'test_ids': created_tests})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def get_test_group(request):
    """Get all tests in a group for editing"""
    if request.method == 'GET':
        test_group = request.GET.get('test_group')
        
        try:
            tests = PatientTest.objects.filter(test_group=test_group).select_related('test_type', 'patient')
            
            tests_data = []
            for test in tests:
                tests_data.append({
                    'test_id': test.test_id,
                    'test_type_name': test.test_type.name,
                    'unit': test.test_type.unit or '',
                    'result_value': test.result_value,
                    'status': test.status,
                    'notes': test.notes or ''
                })
            
            return JsonResponse({
                'success': True,
                'test_group': test_group,
                'patient_name': tests[0].patient.name if tests else '',
                'test_date': tests[0].test_date.strftime('%Y-%m-%d') if tests else '',
                'is_published': tests[0].is_published if tests else False,
                'tests': tests_data
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def update_test_group(request):
    """Update all tests in a group"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        test_group = data.get('test_group')
        tests_data = data.get('tests', [])
        
        try:
            updated_count = 0
            for test_data in tests_data:
                test = PatientTest.objects.get(test_id=test_data['test_id'])
                test.result_value = float(test_data['result_value'])
                test.notes = test_data.get('notes', '')
                test.save()
                updated_count += 1
            
            messages.success(request, f'Updated {updated_count} test(s) successfully!')
            return JsonResponse({'success': True, 'count': updated_count})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def update_test(request):
    if request.method == 'POST':
        test_id = request.POST.get('test_id')
        result_value = request.POST.get('result_value')
        notes = request.POST.get('notes', '')
        
        try:
            test = PatientTest.objects.get(test_id=test_id)
            test.result_value = float(result_value)
            test.notes = notes
            test.save()
            
            return JsonResponse({
                'success': True, 
                'test_id': test.test_id,
                'status': test.status,
                'status_display': test.get_status_display()
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def publish_tests(request):
    if request.method == 'POST':
        test_groups = request.POST.getlist('test_groups[]')
        
        try:
            tests = PatientTest.objects.filter(test_group__in=test_groups)
            
            for test in tests:
                test.is_published = True
                test.published_date = timezone.now()
                test.save()
            
            messages.success(request, f'{len(test_groups)} test group(s) published successfully!')
            return JsonResponse({'success': True, 'count': len(test_groups)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def delete_test(request):
    if request.method == 'POST':
        test_group = request.POST.get('test_group')
        
        try:
            tests = PatientTest.objects.filter(test_group=test_group)
            count = tests.count()
            tests.delete()
            
            messages.success(request, f'Test group with {count} test(s) deleted successfully!')
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def bulk_delete_tests(request):
    if request.method == 'POST':
        test_groups = request.POST.getlist('test_groups[]')
        
        try:
            tests = PatientTest.objects.filter(test_group__in=test_groups)
            total_count = tests.count()
            tests.delete()
            
            messages.success(request, f'{len(test_groups)} test group(s) ({total_count} tests) deleted successfully!')
            return JsonResponse({'success': True, 'count': len(test_groups)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
