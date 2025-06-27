from django.urls import path
from . import views

urlpatterns = [
    path('ask/', views.ask_doctor,name='ask_doctor'),
    path('ask/<int:pk>/answer/', views.answer_question,name='answer_question'),
    path('ask/<int:pk>/', views.question_detail,name='question_detail'),
    path('chat/', views.ask_doctor_chat,name='ask_doctor_chat'),
    path('chat/answer/<int:pk>/', views.answer_question_chat,name='answer_question_chat'),
]