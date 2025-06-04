from django.contrib import admin
from django.contrib.auth.models import User
from .models import Appointment,Doctor,Patient
# Register your models here.

#admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
