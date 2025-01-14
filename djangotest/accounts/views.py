from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Avg, Count
from datetime import timedelta
from django.utils import timezone
from tracker.models import Activity
from reminders.models import Reminder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
import openai  # You'll need to pip install openai
import os

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        # Validate required fields
        if not username:
            messages.error(request, 'Username is required')
            return render(request, 'accounts/signup.html')
            
        if not password:
            messages.error(request, 'Password is required')
            return render(request, 'accounts/signup.html')

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address')
            return render(request, 'accounts/signup.html')
            
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'accounts/signup.html')

        try:
            # Create the user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Log the user in
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'accounts/signup.html')

    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password')
            return render(request, 'accounts/login.html')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'accounts/login.html')
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return redirect('home')

@login_required
def dashboard(request):
    # Get user's activities or return empty queryset if none exist
    activities = Activity.objects.filter(user=request.user).order_by('-date')
    recent_reminders = Reminder.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Initialize context with basic stats
    context = {
        'activities_count': activities.count(),
        'total_calories': sum(a.calories_burned for a in activities if a.calories_burned),
        'recent_reminders': recent_reminders,
        'recent_activities': activities[:5]
    }

    if activities.exists():
        # Calculate additional stats
        avg_heart_rate = activities.aggregate(Avg('heart_rate'))['heart_rate__avg']
        context['avg_heart_rate'] = round(avg_heart_rate) if avg_heart_rate else 0
        context['total_duration'] = sum(a.duration_minutes for a in activities)
        
        # Chart data for the last 7 days
        last_7_days = timezone.now() - timedelta(days=7)
        daily_activities = activities.filter(date__gte=last_7_days)
        
        dates = []
        calories_data = []
        for i in range(7):
            day = timezone.now() - timedelta(days=i)
            day_activities = daily_activities.filter(date__date=day.date())
            dates.insert(0, day.strftime('%b %d'))
            calories_data.insert(0, sum(a.calories_burned or 0 for a in day_activities))
        
        # Activity distribution with case-insensitive grouping
        activity_distribution = {}
        for activity in activities:
            activity_name = activity.name.lower().strip()
            if activity_name in activity_distribution:
                activity_distribution[activity_name] += 1
            else:
                activity_distribution[activity_name] = 1
        
        # Sort and capitalize activity names
        sorted_distribution = sorted(
            activity_distribution.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        activity_types = [name.capitalize() for name, _ in sorted_distribution]
        activity_counts = [count for _, count in sorted_distribution]
        
        # Add chart data to context
        context.update({
            'dates': json.dumps(dates),
            'calories_data': json.dumps(calories_data),
            'activity_types': json.dumps(activity_types),
            'activity_counts': json.dumps(activity_counts)
        })
    else:
        # Set default values if no activities exist
        context.update({
            'avg_heart_rate': 0,
            'total_duration': 0,
            'dates': json.dumps([]),
            'calories_data': json.dumps([]),
            'activity_types': json.dumps([]),
            'activity_counts': json.dumps([])
        })
    
    personal_badges = [
        {'name': 'First Activity', 'description': 'Complete your first activity', 'locked': False},
        {'name': 'Early Bird', 'description': 'Complete 5 morning activities', 'locked': True},
        {'name': 'Calorie Crusher', 'description': 'Burn 1000 calories total', 'locked': True},
    ]
    
    context['personal_badges'] = personal_badges
    
    return render(request, 'accounts/dashboard.html', context)

def team_dashboard(request):
    return render(request, 'accounts/team_dashboard.html')

@login_required
def badges_view(request):
    badge_type = request.GET.get('type', 'personal')
    
    personal_badges = [
        {'name': 'First Activity', 'description': 'Complete your first activity', 'locked': False},
        {'name': 'Early Bird', 'description': 'Complete 5 morning activities', 'locked': True},
        {'name': 'Calorie Crusher', 'description': 'Burn 1000 calories total', 'locked': True},
        {'name': 'Consistency King', 'description': 'Log activities for 7 days straight', 'locked': True},
        {'name': 'Heart Health Hero', 'description': 'Maintain optimal heart rate in 10 activities', 'locked': True},
    ]
    
    team_badges = [
        {'name': 'Team Player', 'description': 'Join your first team', 'locked': True},
        {'name': 'Team Leader', 'description': 'Lead your team to 5000 calories', 'locked': True},
        {'name': 'Team Spirit', 'description': 'Complete 10 team activities', 'locked': True},
        {'name': 'Team Champion', 'description': 'Win a team challenge', 'locked': True},
    ]
    
    context = {
        'badge_type': badge_type,
        'personal_badges': personal_badges,
        'team_badges': team_badges,
    }
    
    return render(request, 'accounts/badges.html', context)

@csrf_protect
@login_required
def chat_message(request):
    if request.method == 'POST':
        try:
            message = request.POST.get('message', '')
            
            # Initialize OpenAI client using environment variable
            client = openai.OpenAI(
                api_key=os.getenv('OPENAI_API_KEY')
            )
            
            # Get response from GPT (new style)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful health and wellness assistant for the HealthHive platform. Provide concise, friendly responses about fitness tracking, health reminders, and wellness goals."},
                    {"role": "user", "content": message}
                ]
            )
            
            # Extract and return the response (new style)
            ai_response = response.choices[0].message.content
            print(f"AI Response: {ai_response}")  # Debug logging
            return JsonResponse({
                'response': ai_response
            })
        except Exception as e:
            print(f"Error in chat_message: {str(e)}")  # Error logging
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
