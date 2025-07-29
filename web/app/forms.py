from django import forms
from .models import Patient, ServiceType, UpdatedFiles
from django.forms import DateInput

class PatientRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg bg-dark text-white border-secondary'
        })
    )

    class Meta:
        model = Patient
        fields = [
            'name', 'username', 'email', 'password', 'birth_date', 'gender',
            'weight', 'height', 'illness', 'drugs', 'surgical_history', 'age'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-dark text-white border-secondary'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-dark text-white border-secondary'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg bg-dark text-white border-secondary'
            }),
            'birth_date': DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-lg bg-dark text-white border-secondary'
            }),
            'gender': forms.Select(choices=[
                ('Kadın', 'Kadın'),
                ('Erkek', 'Erkek'),
                ('Diğer', 'Diğer'),
            ], attrs={
                'class': 'form-control form-control-lg bg-dark text-white border-secondary',
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg bg-dark text-white border-secondary'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg bg-dark text-white border-secondary'
            }),
            'illness': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-dark text-white border-secondary'
            }),
            'drugs': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-dark text-white border-secondary'
            }),
            'surgical_history': forms.Textarea(attrs={
                'class': 'form-control form-control-lg bg-dark text-white border-secondary',
                'rows': 2
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg bg-dark text-white border-secondary'
            }),
        }

class PatientLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg bg-dark text-white border-secondary'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg bg-dark text-white border-secondary'
        })
    )


class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = ['tercih']
        widgets = {
            'tercih': forms.Select(attrs={
                'class': 'form-control form-control-lg bg-dark text-white border-secondary'
            })
        }
        
class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = UpdatedFiles
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary'
            })
        }
    def __init__(self, *args, **kwargs):
        super(PDFUploadForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False  # zorunlu değil
        
class TahlilForm(forms.Form):
    file = forms.FileField(label="PDF Dosyası")