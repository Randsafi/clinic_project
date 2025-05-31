# clinic/serializers.py

from rest_framework import serializers
from clinic.models import Appointment, Patient, Doctor

# أول شي: Serializer للمريض
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'phone','medical_history']  # نختار الحقول اللي بدنا نعرضها

# تاني شي: Serializer للدكتور
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization']

# Serializer الموعد - فيه Nesting للمريض والدكتور
class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date', 'status']
