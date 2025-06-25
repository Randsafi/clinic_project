from django.urls import path
from . import views

urlpatterns = [
    path('ask/', views.ask_doctor,name='ask_doctor'),
    path('questions/<int:pk>/answer/', views.answer_question,name='answer_question'),
    path('questions/<int:pk>/', views.question_detail,name='question_detail'),
    path('chat/', views.ask_doctor_chat,name='ask_doctor_chat'),
]