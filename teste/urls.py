from django.urls import path
from . import views  # لو عندك views

urlpatterns = [
    # هنا تضيف مسارات التطبيق، مثلاً:
    path('all_people', views.all_people, name='all_people'),
    path('all_people/adults/', views.adults, name='adults'),
    path('all_people/teens/', views.teens, name='teens'),
]
