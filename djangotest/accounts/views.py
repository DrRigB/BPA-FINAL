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
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .models import VerificationCode
from .models import Team, TeamMembership
import random
import string
from django.conf import settings

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Validate required fields
        if not username:
            messages.error(request, 'Username is required')
            return render(request, 'accounts/signup.html')
            
        if not password:
            messages.error(request, 'Password is required')
            return render(request, 'accounts/signup.html')
            
        if not email:
            messages.error(request, 'Email is required')
            return render(request, 'accounts/signup.html')
            
        if not confirm_password:
            messages.error(request, 'Please confirm your password')
            return render(request, 'accounts/signup.html')
            
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/signup.html')
            
        # Check password length
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
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
            
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'accounts/signup.html')

        try:
            # Create and save the user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Log the user in immediately
            login(request, user)
            
            # Create success message
            messages.success(request, f'Welcome to HealthHive, {username}!')
            
            # Redirect to dashboard
            return redirect('dashboard')
            
        except Exception as e:
            print(f"Error creating user: {str(e)}")  # Debug logging
            messages.error(request, 'Error creating account. Please try again.')
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
    return redirect('/')  # Redirect to root URL instead of named URL

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

@login_required
def team_dashboard(request):
    team_id = request.GET.get('team_id')
    if not team_id:
        messages.error(request, 'No team selected')
        return redirect('dashboard')
        
    try:
        # Get the team and verify user is a member
        team = Team.objects.get(id=team_id)
        if not TeamMembership.objects.filter(team=team, user=request.user).exists():
            messages.error(request, 'You are not a member of this team')
            return redirect('dashboard')
            
        # Get team members with their roles and activities
        team_members = []
        memberships = TeamMembership.objects.filter(team=team).select_related('user')
        
        for membership in memberships:
            member = membership.user
            member_activities = Activity.objects.filter(user=member).order_by('-date')
            total_calories = sum(a.calories_burned for a in member_activities if a.calories_burned)
            recent_activities = member_activities[:5]
            
            team_members.append({
                'user': member,
                'role': membership.get_role_display(),
                'activities': recent_activities,
                'total_calories': total_calories,
                'total_activities': member_activities.count()
            })
        
        # Get team statistics
        team_activities = Activity.objects.filter(user__teammembership__team=team)
        total_calories = sum(a.calories_burned for a in team_activities if a.calories_burned)
        total_activities = team_activities.count()
        
        context = {
            'team': team,
            'team_members': team_members,
            'total_calories': total_calories,
            'total_activities': total_activities,
        }
        
        return render(request, 'accounts/team_dashboard.html', context)
        
    except Team.DoesNotExist:
        messages.error(request, 'Team not found')
        return redirect('dashboard')

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
            api_key = os.getenv('OPENAI_API_KEY')
            
            if not api_key:
                return JsonResponse({
                    'error': 'OpenAI API key is not set. Please configure the API key in your environment.'
                }, status=400)
            
            try:
                # Initialize OpenAI client with the API key
                client = openai.OpenAI(api_key=api_key)
                
                # Get response from GPT
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful health and wellness assistant for the HealthHive platform. Provide concise, friendly responses about fitness tracking, health reminders, and wellness goals."},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=150
                )
                
                # Extract and return the response
                ai_response = response.choices[0].message.content
                return JsonResponse({'response': ai_response})
                
            except openai.APIError as api_error:
                print(f"OpenAI API Error: {str(api_error)}")  # Debug logging
                return JsonResponse({
                    'error': 'Error communicating with the AI service. Please try again.'
                }, status=500)
                
        except Exception as e:
            print(f"Error in chat_message: {str(e)}")  # Debug logging
            return JsonResponse({
                'error': 'An unexpected error occurred. Please try again.'
            }, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'accounts/password_reset.html')
            
        try:
            user = CustomUser.objects.get(email=email)
            # Generate verification code
            verification = VerificationCode.generate_code(user)
            
            # Send email with verification code
            subject = 'HealthHive Password Reset Code'
            message = f'''Hello {user.username},

Your password reset code is: {verification.code}

This code will expire in 15 minutes. If you did not request this reset, please ignore this email.

Best regards,
The HealthHive Team'''

            try:
                print(f"Attempting to send email to {email}")  # Debug log
                print(f"Using email settings: {settings.EMAIL_HOST_USER}")  # Debug log
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                print("Email sent successfully")  # Debug log
                messages.success(request, 'Verification code has been sent to your email.')
                # Store email in session for verification
                request.session['reset_email'] = email
                return redirect('verify_code')
            except Exception as e:
                print(f"Email sending error: {str(e)}")  # Debug log
                if 'smtp' in str(e).lower():
                    messages.error(request, f'Error with email service: {str(e)}')
                else:
                    messages.error(request, f'Error sending email: {str(e)}')
                return render(request, 'accounts/password_reset.html')
                
        except CustomUser.DoesNotExist:
            # Use a vague message for security
            messages.error(request, 'If an account exists with this email, a reset code will be sent.')
            return render(request, 'accounts/password_reset.html')
    
    return render(request, 'accounts/password_reset.html')

def verify_code(request):
    if 'reset_email' not in request.session:
        messages.error(request, 'Please request a password reset first.')
        return redirect('password_reset')
        
    if request.method == 'POST':
        code = request.POST.get('code', '')
        email = request.session.get('reset_email')
        
        try:
            user = CustomUser.objects.get(email=email)
            verification = VerificationCode.objects.filter(
                user=user,
                code=code,
                is_used=False
            ).latest('created_at')
            
            if verification and verification.is_valid():
                verification.is_used = True
                verification.save()
                # Store user ID in session for password reset
                request.session['reset_user_id'] = user.id
                return redirect('set_new_password')
            else:
                messages.error(request, 'Invalid or expired code.')
        except (CustomUser.DoesNotExist, VerificationCode.DoesNotExist):
            messages.error(request, 'Invalid code.')
        
    return render(request, 'accounts/verify_code.html')

def set_new_password(request):
    if 'reset_user_id' not in request.session:
        messages.error(request, 'Invalid password reset session.')
        return redirect('password_reset')
        
    if request.method == 'POST':
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')
        
        if password1 and password1 == password2:
            try:
                user = CustomUser.objects.get(id=request.session['reset_user_id'])
                user.set_password(password1)
                user.save()
                # Clear session data
                del request.session['reset_email']
                del request.session['reset_user_id']
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Error resetting password.')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'accounts/set_new_password.html')

@login_required
@require_http_methods(["POST"])
def create_team(request):
    try:
        name = request.POST.get('teamName')
        organization = request.POST.get('organization', '')
        description = request.POST.get('teamDescription', '')
        
        if not name:
            return JsonResponse({'error': 'Team name is required'}, status=400)
            
        # Generate a unique 6-character code
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Team.objects.filter(code=code).exists():
                break
        
        # Create the team
        team = Team.objects.create(
            name=name,
            organization=organization,
            description=description,
            code=code,
            leader=request.user
        )
        
        # Add the creator as a team leader
        TeamMembership.objects.create(
            user=request.user,
            team=team,
            role='LEADER'
        )
        
        return JsonResponse({
            'success': True,
            'code': code,
            'teamId': team.id,
            'message': 'Team created successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def join_team(request):
    try:
        code = request.POST.get('teamCode', '').strip().upper()
        
        if not code:
            return JsonResponse({'error': 'Team code is required'}, status=400)
            
        try:
            team = Team.objects.get(code=code)
        except Team.DoesNotExist:
            return JsonResponse({'error': 'Invalid team code'}, status=404)
            
        # Check if user is already a member
        if TeamMembership.objects.filter(user=request.user, team=team).exists():
            return JsonResponse({'error': 'You are already a member of this team'}, status=400)
            
        # Add user as team member
        TeamMembership.objects.create(
            user=request.user,
            team=team,
            role='MEMBER'
        )
        
        return JsonResponse({
            'success': True,
            'teamId': team.id,
            'message': 'Successfully joined the team'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_user_teams(request):
    try:
        # Get teams where user is a member
        memberships = TeamMembership.objects.filter(user=request.user).select_related('team')
        teams = []
        
        for membership in memberships:
            team = membership.team
            teams.append({
                'id': team.id,
                'name': team.name,
                'organization': team.organization,
                'role': membership.role,
                'memberCount': team.members.count(),
                'isLeader': membership.role == 'LEADER'
            })
            
        return JsonResponse({
            'success': True,
            'teams': teams
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def leave_team(request, team_id):
    if request.method == 'POST':
        try:
            team = Team.objects.get(id=team_id)
            membership = TeamMembership.objects.get(user=request.user, team=team)
            
            # Check if user is the team leader
            if membership.role == 'LEADER':
                # If there are other members, assign leadership to another member
                other_member = TeamMembership.objects.filter(team=team).exclude(user=request.user).first()
                if other_member:
                    other_member.role = 'LEADER'
                    other_member.save()
                    team.leader = other_member.user
                    team.save()
                else:
                    # If no other members, delete the team
                    team.delete()
                    messages.success(request, 'Team has been deleted as you were the last member.')
                    return redirect('dashboard')
            
            # Remove user from team
            membership.delete()
            messages.success(request, f'You have successfully left {team.name}.')
            return redirect('dashboard')
            
        except Team.DoesNotExist:
            messages.error(request, 'Team not found.')
        except TeamMembership.DoesNotExist:
            messages.error(request, 'You are not a member of this team.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('dashboard')
