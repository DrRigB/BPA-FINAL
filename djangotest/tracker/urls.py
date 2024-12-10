from django.urls import path
from . import views

urlpatterns = [
    path('activities/', views.activity_list, name='activity_list'),  # List of activities
    path('tracker/', views.track_activity, name='tracker'),  # Activity tracker form
]
