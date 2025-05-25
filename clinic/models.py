from os import name
from django.db import models

# Create your models here.

class Patient(models.Model):
    name =models.CharField(max_length = 100)
    phone =models.CharField(max_length = 15)
    medical_history =models.TextField(max_length = 100)

class Doctor(models.Model):
    name = models.CharField(max_length= 100)
    specialization = models.CharField(max_length= 50)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
