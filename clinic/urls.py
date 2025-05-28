# clinic/urls.py
from django.urls import path
from . import views
from .views import AppointmentListCreate, AppointmentDetail

urlpatterns = [
    path('', views.index,name='index'),
    path('team/', views.team,name='team'),
    path('appointments/', views.appointment_view,name='appointments'),
    path('appointments-page/', views.appointments_view,name='appointments_page'),
    path('appointments/', AppointmentListCreate.as_view()),
    path('appointments/<int:pk>/', AppointmentDetail.as_view()),
]