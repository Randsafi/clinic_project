from django.db import models
from accounts.models import CustomUser 
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class TimeStampeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100 )
    email = models.EmailField(blank=True, null=True)  # أضفت الإيميل
    phone = models.CharField(max_length=15)  # غيرت الاسم من phone إلى mobile ليتطابق مع الفورم
    medical_history = models.TextField(blank=True, null=True)  # خليتها اختيارية

    def __str__(self):
        return self.firstname
    
class Department(models.Model):
    specialization = models.CharField(max_length=50)
    details = models.TextField()
    def __str__(self):
        return self.specialization

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE , null=True, blank=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100 )
    img = models.ImageField(upload_to='doctors/', blank=True, null=True)  # حطيت upload_to
    #specialization = models.CharField(max_length=50)
    specialization= models.ForeignKey(Department,  on_delete=models.CASCADE, null=True, blank=True)
    is_experience = models.BooleanField(_("Has Experience"), default=False)
    phone = models.CharField(max_length=15)
    facebook = models.CharField(max_length=100 , blank=True , null=True)
    twitter  = models.CharField(max_length=100 , blank=True , null=True)
    instagram = models.CharField(max_length=100 , blank=True , null=True)

    def __str__(self):
        return self.firstname

class Appointment(TimeStampeModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
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
        return f"Appointment for {self.patient.firstname} with {self.doctor.firstname} on {self.date.strftime('%Y-%m-%d %H:%M')}"

class MedicalReport(TimeStampeModel): 
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reports')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_reports',
        limit_choices_to={'user_type__in': ['doctor', 'assistant']}
    )
    content = models.TextField(verbose_name="Report content")
    notes = models.TextField(blank=True, null=True, verbose_name="Additional Notes")
    appointment = models.ForeignKey('Appointment', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"تقرير طبي للمريض {self.patient} date {self.created_at.strftime('%Y-%m-%d')}"