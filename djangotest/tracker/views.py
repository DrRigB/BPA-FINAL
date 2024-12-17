from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Activity
from .forms import ActivityForm
from django.contrib import messages

@login_required
def activity_list(request):
    activities = Activity.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/activity_list.html', {'activities': activities})

@login_required
def add_activity(request):
    if request.method == 'POST':
        try:
            activity = Activity(
                user=request.user,
                name=request.POST['name'],
                duration_minutes=int(request.POST['duration_minutes']),
                heart_rate=int(request.POST['heart_rate'])
            )
            activity.save()
            messages.success(request, 'Activity added successfully!')
            return redirect('activity_list')
        except ValueError as e:
            messages.error(request, str(e))
    return render(request, 'tracker/add_activity.html')

@login_required
def edit_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == 'POST':
        try:
            activity.name = request.POST['name']
            activity.duration_minutes = int(request.POST['duration_minutes'])
            activity.heart_rate = int(request.POST['heart_rate'])
            activity.save()
            messages.success(request, 'Activity updated successfully!')
            return redirect('activity_list')
        except ValueError as e:
            messages.error(request, str(e))
    return render(request, 'tracker/edit_activity.html', {'activity': activity})

@login_required
def delete_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Activity deleted successfully!')
        return redirect('activity_list')
    return render(request, 'tracker/delete_activity.html', {'activity': activity})
