from django.shortcuts import render
from rest_framework import generics
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentListCreate(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

def index(request):
    return render(request , 'temp/index.html')

def appointments_view(request):
    return render(request, 'test.html')
