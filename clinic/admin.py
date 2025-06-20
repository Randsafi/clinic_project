from django.contrib import admin
from django.contrib.auth.models import User
from .models import Appointment,Doctor,Patient,Department,MedicalReport
# Register your models here.

admin.site.register(Department)
admin.site.register(Doctor)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'medical_history')
    search_fields = ('first_name', 'phone')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    full_name.short_description = 'Name'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'status')  # أعمدة جدول العرض
    list_filter = ('status', 'doctor')                      # فلترة جانبية
    search_fields = ('patient__name', 'doctor__name')       # حقل بحث
    ordering = ('-date',)                                   # ترتيب افتراضي
    list_editable = ('status',)                             # تعديل مباشر من الجدول
    date_hierarchy = 'date'                                 # تصفح حسب التاريخ

@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'created_by', 'appointment')
    list_filter = ('patient',)  # لازم تكون tuple أو list
    search_fields = ('patient__name', 'created_by__username')
