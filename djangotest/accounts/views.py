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

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Add validation to ensure username is provided
        if not username:
            return render(request, 'accounts/signup.html', {
                'error': 'Username is required'
            })
            
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'accounts/signup.html', {
                'error': 'Username already exists'
            })

        try:
            # Create the user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Log the user in
            login(request, user)
            return redirect('home')  # Redirect to home page after successful signup
        except ValueError as e:
            return render(request, 'accounts/signup.html', {
                'error': str(e)
            })

    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'error_message': 'Invalid credentials'})
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
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
        
        # Activity distribution
        activity_distribution = activities.values('name').annotate(count=Count('id'))
        activity_types = [item['name'] for item in activity_distribution]
        activity_counts = [item['count'] for item in activity_distribution]
        
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
    
    return render(request, 'accounts/dashboard.html', context)

def team_dashboard(request):
    return render(request, 'accounts/team_dashboard.html')