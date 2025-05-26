# clinic/urls.py
from django.urls import path
from . import views
from .views import AppointmentListCreate, AppointmentDetail

urlpatterns = [
    path('', views.index,name='appointments_page'),
    path('appointments-page/', views.appointments_view,name='appointments_page'),
    path('appointments/', AppointmentListCreate.as_view()),
    path('appointments/<int:pk>/', AppointmentDetail.as_view()),
]