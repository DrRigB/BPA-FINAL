from django.shortcuts import render, redirect
from .models import Activity
from .forms import ActivityForm
from django.shortcuts import get_object_or_404



def activity_list(request):
    activities = Activity.objects.all()  # Get all activities to display
    return render(request, 'tracker/activity_list.html', {'activities': activities, 'form': ActivityForm()})

def track_activity(request):
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.calculate_calories_burned()  # Calculate the calories burned
            activity.save()
            return redirect('activity_list')  # Redirect to the activity list page after saving
    else:
        form = ActivityForm()

    activities = Activity.objects.all()  # Get all activities to display
    return render(request, 'tracker/activity_list.html', {'form': form, 'activities': activities})

def delete_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        activity.delete()
        return redirect('activity_list')
