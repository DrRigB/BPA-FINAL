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
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            messages.success(request, 'Activity added successfully!')
            return redirect('activity_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ActivityForm()
    return render(request, 'tracker/add_activity.html', {'form': form})

@login_required
def edit_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity updated successfully!')
            return redirect('activity_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'tracker/edit_activity.html', {'form': form, 'activity': activity})

@login_required
def delete_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Activity deleted successfully!')
        return redirect('activity_list')
    return render(request, 'tracker/delete_activity.html', {'activity': activity})
