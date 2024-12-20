from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('team-dashboard/', views.team_dashboard, name='team_dashboard'),
    path('badges/', views.badges_view, name='badges'),
    path('chat/', views.chat_message, name='chat_message'),
]