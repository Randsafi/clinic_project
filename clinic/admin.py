from django.contrib import admin
from .models import Appointment,Doctor,Patient,Department
# Register your models here.

admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
