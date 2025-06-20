from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Appointment,Patient ,Doctor
from .forms import AppointmentForm
from datetime import datetime,time,timedelta
from django.utils import timezone

User = get_user_model()

def get_available_slots(doctor, date):
    start_time = time(9, 0)
    end_time = time(17, 0)
     # أنشئ قائمة جميع الفترات المحتملة
    slots = []
    current = datetime.combine(date, start_time)
    end_datetime = datetime.combine(date, end_time)

    while current < end_datetime:
        slots.append(current)
        current += timedelta(hours=1)
    # جلب مواعيد الطبيب في هذا اليوم
    booked_appointments = Appointment.objects.filter(
        doctor=doctor,
        date__date=date  # نفس اليوم فقط
    ).values_list('date', flat=True)
    # استبعاد الأوقات المحجوزة
    available_slots = [slot for slot in slots if slot not in booked_appointments]

    return available_slots

def index(request):
    
    return render(request, 'temp/index.html')

def team(request):
    doctors = Doctor.objects.all()
    return render(request,'temp/Team.html' , {'doctors':doctors})  

def about(request):
    return render(request, 'temp/about.html')

def contect(request):
    return render(request, 'temp/about.html')

def appointment_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            datetime = form.cleaned_data['datetime']
            doctor = form.cleaned_data['doctor']
            problem = form.cleaned_data['problem_description']

            # محاولة الحصول على المستخدم أو إنشائه
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0] + get_random_string(4),
                    'first_name': name.split()[0],
                    'last_name': ' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
                    'user_type': 'patient',
                }
            )

            # إذا أنشأناه جديد، لازم نضيف له كلمة سر
            if created:
                random_password = User.objects.make_random_password()
                user.set_password(random_password)
                user.save()
                # يمكن إرسال كلمة السر للمريض عبر البريد أو إشعار (اختياري)

            # ربط أو إنشاء المريض
            patient, _ = Patient.objects.get_or_create(
                user=user,
                defaults={
                    'firstname': user.first_name,
                    'lastname': user.last_name,
                    'phone': phone
                }
            )

            # حجز الموعد إن لم يكن محجوزًا
            if Appointment.objects.filter(doctor=doctor, date=datetime).exists():
                messages.error(request, 'هذا الموعد محجوز مسبقًا.')
            else:
                Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    date=datetime,
                    problem_description=problem,
                    status='pending'
                )
                messages.success(request, 'تم حجز الموعد وإنشاء حساب لك بنجاح!')
                return redirect('appointments')

        else:
            print("Form errors:", form.errors)

    else:
        form = AppointmentForm()

    return render(request, 'temp/appointment.html', {'form': form})

def booked_slots_json(request, doctor_id):
    appointments = Appointment.objects.filter(doctor_id=doctor_id).values_list('date', flat=True)
    # نرجعهم على شكل string منسق
    data = [dt.strftime('%Y-%m-%d %H:%M') for dt in appointments]
    return JsonResponse(data, safe=False)

def service(request):
    
    return render(request,'temp/service.html')
