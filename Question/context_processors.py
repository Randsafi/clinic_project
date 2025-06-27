from django.shortcuts import get_object_or_404
from .models import Notification, Question
from clinic.models import Doctor,Patient
from .forms import Question_chatForm,Answer_chatForm

def notifications_processor(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(is_read=False)
        return {
            'notifications': notifications,
            'notifications_count': notifications.count()
        }
    return {
        'notifications': [],
        'notifications_count': 0
    }

# context_processors.py

def doctor_chat_context(request):
    if request.user.is_authenticated and request.user.user_type == 'patient':
        form = Question_chatForm()
        questions = Question.objects.filter(patient=request.user).order_by('-id')[:10]
    else:
        form = None
        questions = []

    return {
        'patient_chat_form': form,
        'chat_questions': questions,
    }

def ansewr_doctor(request):
    if request.user.is_authenticated and request.user.user_type == 'doctor':
        form = Answer_chatForm()
        ansewrs = Question.objects.filter(doctor=request.user).order_by('-id')[:10]
    else:
        form = None
        ansewrs = []
    return {
        'doctor_chat_form': form,
        'chat_ansewrs':ansewrs
    }