from django.urls import path
from . import views

urlpatterns = [
    path('', views.ask_doctor,name='ask_doctor')
]