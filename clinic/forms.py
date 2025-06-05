from django import forms
from .models import Doctor ,Patient

class AppointmentForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control border-0',
            'placeholder': 'Your Name',
            'style': 'height: 55px;'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control border-0',
            'placeholder': 'Your Email',
            'style': 'height: 55px;'
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control border-0',
            'placeholder': 'Your Mobile',
            'style': 'height: 55px;'
        })
    )

    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select border-0',
            'style': 'height: 50px;'
        })
    )

    datetime = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.TextInput(attrs={
            'class': 'form-control border-0 datetimepicker-input',
            'placeholder': 'Choose Date',
            'data-target': '#date',
            'data-toggle': 'datetimepicker',
            'style': 'height: 55px;',
        })
    )
    problem_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control border-0',
            'rows': 5,
            'placeholder': 'Describe your problem'
        })
    )

