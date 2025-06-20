from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('receptionist', 'receptionist'),
        ('assistant', 'assistant'),
    )
    user_type = models.CharField(max_length=12, choices=USER_TYPE_CHOICES)

    def __str__(self):
        if self.user_type == 'doctor':
            if self.first_name and self.last_name:
                return f"Dr. {self.first_name} {self.last_name}"
            return f"Dr. {self.username}"
        return self.username

