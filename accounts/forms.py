from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from clinic.models import Doctor ,Patient

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username' , 'email', 'user_type', 'password1' , 'password2'
        )
        help_texts={
            'username': 'Enter a 12-letter name'
        }
        
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['img','firstname','lastname' , 'specialization','is_experience','phone','facebook','twitter','instagram']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['firstname','lastname' , 'email','phone','medical_history']
        widgets ={
            'medical_history': forms.Textarea(attrs={
                'placeholder': 'Do you have a medical history?'})
        }