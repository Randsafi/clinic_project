from django.urls import path
from . import views

urlpatterns = [
    path('', views.ask_doctor,name='ask_doctor'),
    path('', views.answer_question,name='answer_question'),
    path('', views.question_detail,name='question_detail'),
]