# tracker/models.py
from django.db import models

class Activity(models.Model):
    name = models.CharField(max_length=255, default="Exercise")
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField(help_text="Duration of the activity in minutes")
    heart_rate = models.IntegerField(help_text="Average heart rate during the exercise")
    calories_burned = models.IntegerField(blank=True, null=True)  # We'll calculate this
    date = models.DateTimeField(auto_now_add=True)

    def calculate_calories_burned(self):
        # Simple formula for calories burned: calories = duration * heart_rate * factor
        # You can refine this formula based on actual data
        factor = 0.063  # A general factor for calorie estimation
        self.calories_burned = int(self.duration_minutes * self.heart_rate * factor)
        self.save()

    def __str__(self):
        return f"{self.name} - {self.date}"
