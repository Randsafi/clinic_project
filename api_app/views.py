from django.shortcuts import render
from rest_framework import generics
from clinic.models import Appointment
from api_app.serializers import AppointmentSerializer

# Create your views here.
class AppointmentListCreate(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


def appointments_view(request):
    return render(request, 'test.html')