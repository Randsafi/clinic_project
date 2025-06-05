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

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['img','firstname','lastname' , 'specialization','is_experience','phone','facebook','twitter','instagram']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['firstname','lastname' , 'email','phone']