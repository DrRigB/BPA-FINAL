from django.urls import path
from . import views

urlpatterns = [
    path('', views.reminder_list, name='reminder_list'),
    path('add/', views.add_reminder, name='add_reminder'),
    path('toggle/<int:pk>/', views.toggle_reminder, name='toggle_reminder'),
] 