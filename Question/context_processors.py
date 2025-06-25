from django.shortcuts import get_object_or_404
from .models import Notification, Question
from clinic.models import Doctor,Patient
from .forms import Question_chatForm

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
    form = None
    questions = []

    if request.user.is_authenticated:
        try:
            #patient = Patient.objects.get(user=request.user)  # OneToOne relation from user to Patient
            questions = Question.objects.filter(patient=request.user).order_by('-id')[:10]
            form = Question_chatForm()
        except Patient.DoesNotExist:
            form = None
            questions = []
    else:
        form = None
        questions = []

    return {
        'chat_form': form,
        'chat_questions': questions,
    }