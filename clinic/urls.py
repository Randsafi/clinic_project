# clinic/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('team/', views.team,name='team'),
    path('about/', views.about,name='about'),
    path('contect/', views.contect,name='contect'),
    path('appointments/', views.appointment_view,name='appointments'),
    path('service/', views.service,name='service'),
]