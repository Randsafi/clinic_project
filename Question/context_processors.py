from django.shortcuts import get_object_or_404
from .models import Notification, Question
from .forms import Question_chatForm, Answer_chatForm

# إشعارات المستخدم (تُستخدم في كل الصفحات)
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

# فقاعة الشات الخاصة بالمريض
def patient_chat_context(request):
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

# فقاعة الشات الخاصة بالطبيب
def doctor_chat_context(request):
    if request.user.is_authenticated and request.user.user_type == 'doctor':
        form = Answer_chatForm()
        answers = Question.objects.filter(doctor=request.user).order_by('-id')[:10]
    else:
        form = None
        answers = []

    return {
        'doctor_chat_form': form,
        'chat_answers': answers
    }
