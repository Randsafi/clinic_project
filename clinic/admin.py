from django.contrib import admin
from django.contrib.auth.models import User
from .models import Appointment,Doctor,Patient,Department,MedicalReport
# Register your models here.

admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Patient)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'status')
    list_filter = ('status', 'doctor')
    search_fields = (
        'patient__firstname',
        'patient__lastname',
        'doctor__firstname',
        'doctor__lastname',
    )
    ordering = ('-date',)
    list_editable = ('status',)
    date_hierarchy = 'date'


@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'created_by', 'appointment')
    list_filter = ('patient',)
    search_fields = (
        'patient__firstname',
        'patient__lastname',
        'created_by__username',
    )
