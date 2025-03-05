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
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    path('create-team/', views.create_team, name='create_team'),
    path('join-team/', views.join_team, name='join_team'),
    path('get-user-teams/', views.get_user_teams, name='get_user_teams'),
    path('leave-team/<int:team_id>/', views.leave_team, name='leave_team'),
]