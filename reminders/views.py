from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Reminder
from .forms import ReminderForm

@login_required
def reminder_list(request):
    reminders = Reminder.objects.filter(user=request.user)
    return render(request, 'reminders/reminder_list.html', {'reminders': reminders})

@login_required
def add_reminder(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            return redirect('reminder_list')
    else:
        form = ReminderForm()
    return render(request, 'reminders/add_reminder.html', {'form': form})

@login_required
def toggle_reminder(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    reminder.is_completed = not reminder.is_completed
    if reminder.is_completed:
        reminder.last_completed = timezone.now()
    reminder.save()
    return redirect('reminder_list') 