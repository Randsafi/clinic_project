from django.contrib import messages
from django.shortcuts import render,redirect
from rest_framework import generics
from .models import Appointment,Patient ,Doctor
from .serializers import AppointmentSerializer
from .forms import AppointmentForm


def index(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم حجز الموعد بنجاح! سنتواصل معك قريبًا.')
            return render(request, 'temp/index.html')
    else:
        form = AppointmentForm()

    return render(request, 'temp/index.html', {'form': form})

def team(request):
    doctors = Doctor.objects.all()
    return render(request,'temp/Team.html' , {'doctors':doctors})  

def about(request):
    return render(request, 'temp/about.html')

def contect(request):
    return render(request, 'temp/about.html')

def appointment_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # حفظ بيانات المريض
            patient, created = Patient.objects.get_or_create(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                defaults={'medical_history': ''}
            )

            # حفظ الموعد
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=form.cleaned_data['doctor'],
                date=form.cleaned_data['datetime'],
                status='pending'
            )
            print("VALID:", form.errors)
            messages.success(request, 'تم حجز الموعد بنجاح!')
            return redirect('appointments')
        else:
            print("INVALID:", form.errors)
    else:
        form = AppointmentForm()

    return render(request, 'temp/appointment.html', {'form': form})

class AppointmentListCreate(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


def appointments_view(request):
    return render(request, 'test.html')
