from os import name
from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)  # أضفت الإيميل
    phone = models.CharField(max_length=15)  # غيرت الاسم من phone إلى mobile ليتطابق مع الفورم
    medical_history = models.TextField(blank=True, null=True)  # خليتها اختيارية

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='doctors/', blank=True, null=True)  # حطيت upload_to
    specialization = models.CharField(max_length=50)
    facebook = models.CharField(max_length=100 , blank=True , null=True)
    X = models.CharField(max_length=100 , blank=True , null=True)
    instagram = models.CharField(max_length=100 , blank=True , null=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()  # هنا التاريخ والوقت مع بعض، أنسب من فصلهم
    problem_description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )

    def __str__(self):
        return f"Appointment for {self.patient.name} with {self.doctor.name} on {self.date.strftime('%Y-%m-%d %H:%M')}"
