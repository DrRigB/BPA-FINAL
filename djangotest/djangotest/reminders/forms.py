from django import forms
from .models import Reminder

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'description', 'frequency', 'time']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
        } 