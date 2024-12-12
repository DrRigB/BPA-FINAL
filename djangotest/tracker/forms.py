from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'duration_minutes', 'heart_rate']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Activity Name'}),
            'duration_minutes': forms.NumberInput(attrs={'placeholder': 'Duration (in minutes)'}),
            'heart_rate': forms.NumberInput(attrs={'placeholder': 'Heart Rate (bpm)'}),
        }
