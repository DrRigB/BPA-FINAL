from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'duration_minutes', 'heart_rate']
        widgets = {
            'duration_minutes': forms.NumberInput(attrs={
                'min': '1',
                'max': '300',
                'required': True,
            }),
            'heart_rate': forms.NumberInput(attrs={
                'min': '40',
                'max': '220',
                'required': True,
            })
        }

