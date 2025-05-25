# clinic/urls.py
from django.urls import path
from .views import AppointmentListCreate, AppointmentDetail

urlpatterns = [
    path('appointments/', AppointmentListCreate.as_view()),
    path('appointments/<int:pk>/', AppointmentDetail.as_view()),
]