from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import Patient, MedicalReport, TestCategory, TestType, PatientTest, LabSettings
from .forms import PatientForm, MedicalReportForm
from django.conf import settings as django_settings
from django.contrib.auth.models import User
import random
import os
import re
import string
from functools import wraps
from openai import OpenAI


def admin_required(view_func):
    """Decorator to ensure only admin/staff users can access a view, not patients"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        # If user is a patient, redirect to patient portal
        if hasattr(request.user, 'patient_profile'):
            messages.error(request, 'Access denied. This area is for administrators only.')
            return redirect('patient_portal')
        return view_func(request, *args, **kwargs)
    return wrapper

def login_view(request):
    if request.user.is_authenticated:
        # Check if user is a patient and redirect to patient portal
        if hasattr(request.user, 'patient_profile'):
            return redirect('patient_portal')
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Check if user is a patient and redirect accordingly
            if hasattr(user, 'patient_profile'):
                return redirect('patient_portal')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@admin_required
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
@admin_required
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
@admin_required
def edit_patient(request):
    if request.method == 'POST':
        try:
            patient_id = request.POST.get('patient_id')
            patient = get_object_or_404(Patient, id=patient_id)
            
            form = PatientForm(request.POST, instance=patient)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Patient updated successfully!'})
            else:
                return JsonResponse({'success': False, 'error': str(form.errors)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@admin_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            # Generate random password for the patient
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            patient = form.save(commit=False)
            patient.password = password  # Store password in Patient model
            
            # Create a Django User for the patient using contact_number as username
            try:
                user = User.objects.create_user(
                    username=patient.contact_number,
                    password=password,
                    first_name=patient.name.split()[0] if patient.name else '',
                    last_name=' '.join(patient.name.split()[1:]) if len(patient.name.split()) > 1 else ''
                )
                patient.user = user
                patient.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': f'Patient added successfully! Login credentials - Mobile: {patient.contact_number}, Password: {password}'
                    })
                
                messages.success(request, f'Patient added successfully! Login credentials - Mobile: {patient.contact_number}, Password: {password}')
                return redirect('dashboard')
            except Exception as e:
                patient.delete()  # Rollback patient creation if user creation fails
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'errors': {'error': str(e)}
                    })
                messages.error(request, f'Error creating patient: {str(e)}')
                return redirect('patients')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
@admin_required
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
    
    # Get all patients for the add report modal
    all_patients = Patient.objects.all()
    
    context = {
        'reports': reports,
        'status_filter': status_filter,
        'search_query': search_query,
        'all_patients': all_patients,
    }
    return render(request, 'reports.html', context)

@login_required
@admin_required
def report_detail(request, report_id):
    report = get_object_or_404(MedicalReport, report_id=report_id)
    lab_settings = LabSettings.get_settings()
    
    # Get published test groups for THIS SPECIFIC REPORT
    from collections import defaultdict
    all_tests = PatientTest.objects.filter(
        report=report,
        is_published=True
    ).select_related('test_type', 'test_type__category').order_by('-test_date', 'test_group')
    
    # Group tests by test_group
    test_groups = defaultdict(list)
    for test in all_tests:
        test_groups[test.test_group].append(test)
    
    context = {
        'report': report,
        'test_groups': list(test_groups.values()),
        'lab_settings': lab_settings,
    }
    return render(request, 'report_detail.html', context)


@login_required
@admin_required
def add_report(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        content = request.POST.get('content', '')
        diagnosis = request.POST.get('diagnosis', '')
        recommendations = request.POST.get('recommendations', '')
        
        try:
            patient = Patient.objects.get(id=patient_id)
            
            # Create new report
            report = MedicalReport.objects.create(
                patient=patient,
                status='normal',  # Default status, can be updated later
                ai_generated=False,
                created_by=request.user,
                content=content,
                diagnosis=diagnosis,
                recommendations=recommendations
            )
            
            messages.success(request, f'Report {report.report_id} created successfully!')
            return JsonResponse({'success': True, 'report_id': report.report_id})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Patient not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@admin_required
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
@admin_required
def tests_view(request):
    # Get all test categories with their test types
    categories = TestCategory.objects.prefetch_related('test_types').all()
    
    # Get all patients for the dropdown
    patients = Patient.objects.all()
    
    # Get all patient tests grouped by test_group
    all_tests = PatientTest.objects.select_related('patient', 'test_type', 'test_type__category', 'report').order_by('-test_date', 'test_group')
    
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
@admin_required
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
                    report=None,  # No report until published
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
def publish_tests(request):
    if request.method == 'POST':
        test_groups = request.POST.getlist('test_groups[]')
        
        try:
            for test_group in test_groups:
                tests = PatientTest.objects.filter(test_group=test_group)
                
                if tests.exists():
                    # Get the patient from the first test
                    first_test = tests.first()
                    patient = first_test.patient
                    
                    # Generate report ID
                    last_report = MedicalReport.objects.all().order_by('id').last()
                    if last_report:
                        last_num = int(last_report.report_id.split('-')[1])
                        report_id = f'REP-{str(last_num + 1).zfill(3)}'
                    else:
                        report_id = 'REP-001'
                    
                    # Collect test summary for report content
                    test_summary = []
                    for test in tests:
                        test_summary.append(f"{test.test_type.name}: {test.result_value} {test.test_type.unit} ({test.status})")
                    
                    content = "Laboratory Test Report\\n\\n" + "\\n".join(test_summary)
                    
                    # Determine overall status based on test statuses
                    if any(t.status == 'critical' for t in tests):
                        overall_status = 'critical'
                    elif any(t.status == 'abnormal' for t in tests):
                        overall_status = 'at_risk'
                    else:
                        overall_status = 'normal'
                    
                    # Create new report
                    report = MedicalReport.objects.create(
                        report_id=report_id,
                        patient=patient,
                        content=content,
                        diagnosis=f"Test Group {test_group} - {overall_status.upper()}",
                        recommendations="Please review test results with a healthcare provider.",
                        status=overall_status,
                        ai_generated=False,
                        created_by=request.user
                    )
                    
                    # Link tests to the new report and publish them
                    tests.update(
                        report=report,
                        is_published=True,
                        published_date=timezone.now()
                    )
            
            messages.success(request, f'{len(test_groups)} test group(s) published with new report(s)!')
            return JsonResponse({'success': True, 'count': len(test_groups)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
@admin_required
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
@admin_required
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


@login_required
@admin_required
def delete_report(request, report_id):
    if request.method == 'POST':
        try:
            report = MedicalReport.objects.get(report_id=report_id)
            # Delete associated tests first (cascade should handle this, but being explicit)
            PatientTest.objects.filter(report=report).delete()
            # Delete the report
            report.delete()
            messages.success(request, f'Report {report_id} deleted successfully!')
            return JsonResponse({'success': True})
        except MedicalReport.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Report not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
@admin_required
def bulk_delete_reports(request):
    if request.method == 'POST':
        report_ids = request.POST.getlist('report_ids[]')
        
        try:
            # Delete all associated tests first
            for report_id in report_ids:
                report = MedicalReport.objects.get(report_id=report_id)
                PatientTest.objects.filter(report=report).delete()
                report.delete()
            
            messages.success(request, f'{len(report_ids)} report(s) deleted successfully!')
            return JsonResponse({'success': True, 'count': len(report_ids)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
@admin_required
def delete_patient(request, patient_id):
    if request.method == 'POST':
        try:
            patient = Patient.objects.get(id=patient_id)
            # Delete all reports and tests associated with this patient
            reports = MedicalReport.objects.filter(patient=patient)
            for report in reports:
                PatientTest.objects.filter(report=report).delete()
            reports.delete()
            # Delete the patient
            patient.delete()
            messages.success(request, f'Patient deleted successfully!')
            return JsonResponse({'success': True})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Patient not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
@admin_required
def bulk_delete_patients(request):
    if request.method == 'POST':
        patient_ids = request.POST.getlist('patient_ids[]')
        
        try:
            for patient_id in patient_ids:
                patient = Patient.objects.get(id=patient_id)
                # Delete all reports and tests associated with this patient
                reports = MedicalReport.objects.filter(patient=patient)
                for report in reports:
                    PatientTest.objects.filter(report=report).delete()
                reports.delete()
                patient.delete()
            
            messages.success(request, f'{len(patient_ids)} patient(s) deleted successfully!')
            return JsonResponse({'success': True, 'count': len(patient_ids)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
@admin_required
def generate_ai_report(request, report_id):
    if request.method == 'POST':
        try:
            report = MedicalReport.objects.get(report_id=report_id)
            
            # Get all test results for this report
            tests = PatientTest.objects.filter(report=report, is_published=True).select_related('test_type', 'test_type__category')
            
            # Build test results data for AI
            test_data = []
            critical_tests = []
            abnormal_tests = []
            
            for test in tests:
                test_info = {
                    'category': test.test_type.category.name,
                    'name': test.test_type.name,
                    'value': test.result_value,
                    'unit': test.test_type.unit,
                    'normal_min': test.test_type.normal_range_min,
                    'normal_max': test.test_type.normal_range_max,
                    'status': test.status
                }
                test_data.append(test_info)
                
                if test.status == 'critical':
                    critical_tests.append(test.test_type.name)
                elif test.status == 'abnormal':
                    abnormal_tests.append(test.test_type.name)
            
            # Prepare patient context
            patient = report.patient
            patient_context = f"""Patient Information:
- Age: {patient.age}
- Gender: {patient.gender}
- Contact: {patient.contact_number}"""
            
            # Format test results for AI
            test_results_text = "\n".join([
                f"- {t['category']} - {t['name']}: {t['value']} {t['unit']} "
                f"(Normal: {t['normal_min']}-{t['normal_max']}, Status: {t['status'].upper()}"
                for t in test_data
            ])
            
            # Initialize OpenAI client
            client = OpenAI(api_key=django_settings.OPENAI_API_KEY)
            
            # Create AI prompt
            prompt = f"""You are a medical AI assistant analyzing laboratory test results. 
Provide a professional medical report in HTML format.

{patient_context}

Laboratory Test Results:
{test_results_text}

Please provide:
1. **Clinical Assessment** (diagnosis section): Analyze the test results, identify critical, abnormal, and normal findings. Provide medical interpretation.
2. **Medical Recommendations**: Specific recommendations based on the findings, including urgency of follow-up, lifestyle changes, and further tests if needed.

Format your response in clean HTML with <h4>, <p>, <strong>, <ol>, <li> tags. Be professional and medically accurate.

Separate the two sections clearly with the headers "Clinical Assessment" and "Medical Recommendations"."""

            # Call OpenAI ChatGPT API
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a professional medical AI assistant that analyzes laboratory test results and provides clinical assessments and recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Extract AI response
            ai_response = response.choices[0].message.content
            
            # Split response into diagnosis and recommendations
            # Try to split by common patterns
            if "Medical Recommendations" in ai_response:
                parts = ai_response.split("Medical Recommendations")
                diagnosis = parts[0].replace("Clinical Assessment", "").strip()
                recommendations = "<h4>Medical Recommendations</h4>" + parts[1].strip()
            elif "**Medical Recommendations**" in ai_response:
                parts = ai_response.split("**Medical Recommendations**")
                diagnosis = parts[0].replace("**Clinical Assessment**", "").replace("Clinical Assessment", "").strip()
                recommendations = "<h4>Medical Recommendations</h4>" + parts[1].strip()
            else:
                # Fallback if AI doesn't split properly
                diagnosis = ai_response
                recommendations = "<p>Please consult with your healthcare provider for personalized recommendations.</p>"
            
            # Determine overall status
            if critical_tests:
                overall_status = 'critical'
            elif abnormal_tests:
                overall_status = 'at_risk'
            else:
                overall_status = 'normal'
            
            # Update report
            report.diagnosis = diagnosis
            report.recommendations = recommendations
            report.status = overall_status
            report.ai_generated = True
            report.save()
            
            messages.success(request, 'AI report generated successfully!')
            return JsonResponse({
                'success': True,
                'diagnosis': diagnosis,
                'recommendations': recommendations,
                'status': overall_status
            })
            
        except MedicalReport.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Report not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'AI generation failed: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# Patient Portal Views
def patient_portal(request):
    """Portal view for patients to see their reports"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Check if user is a patient
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Access denied. This portal is only for patients.')
        return redirect('login')
    
    patient = request.user.patient_profile
    reports = MedicalReport.objects.filter(patient=patient).order_by('-date_created')
    
    context = {
        'patient': patient,
        'reports': reports,
    }
    return render(request, 'patient_portal.html', context)


def patient_report_detail(request, report_id):
    """View for patients to see detailed report"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Check if user is a patient
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Access denied.')
        return redirect('login')
    
    patient = request.user.patient_profile
    report = get_object_or_404(MedicalReport, report_id=report_id, patient=patient)
    lab_settings = LabSettings.get_settings()
    
    # Get published test groups for THIS SPECIFIC REPORT
    from collections import defaultdict
    all_tests = PatientTest.objects.filter(
        report=report,
        is_published=True
    ).select_related('test_type', 'test_type__category').order_by('-test_date', 'test_group')
    
    # Group tests by test_group
    test_groups = defaultdict(list)
    for test in all_tests:
        test_groups[test.test_group].append(test)
    
    context = {
        'report': report,
        'test_groups': list(test_groups.values()),
        'lab_settings': lab_settings,
        'is_patient_view': True,
    }
    return render(request, 'report_detail.html', context)


def patient_logout_view(request):
    """Logout view for patients"""
    logout(request)
    return redirect('login')

@login_required
@admin_required
def settings_view(request):
    settings = LabSettings.get_settings()
    
    if request.method == 'POST':
        settings.lab_name = request.POST.get('lab_name', settings.lab_name)
        settings.lab_address = request.POST.get('lab_address', settings.lab_address)
        settings.lab_phone = request.POST.get('lab_phone', '')
        settings.lab_email = request.POST.get('lab_email', '')
        
        # Handle logo upload
        if 'lab_logo' in request.FILES:
            settings.lab_logo = request.FILES['lab_logo']
        
        settings.updated_by = request.user
        settings.save()
        
        messages.success(request, 'Lab settings updated successfully!')
        return redirect('settings')
    
    context = {
        'settings': settings,
    }
    return render(request, 'settings.html', context)
