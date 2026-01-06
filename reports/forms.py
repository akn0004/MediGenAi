from django import forms
from .models import Patient, MedicalReport

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'contact_number']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sarah Smith'
            }),
            'age': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[(i, i) for i in range(1, 121)]),
            'gender': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '9876543210',
                'pattern': '[6-9][0-9]{9}',
                'maxlength': '10',
                'type': 'tel',
                'title': 'Please enter a valid 10-digit Indian mobile number starting with 6-9'
            }),
        }

class MedicalReportForm(forms.ModelForm):
    class Meta:
        model = MedicalReport
        fields = ['patient', 'status', 'content', 'diagnosis', 'recommendations', 'ai_generated']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ai_generated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
