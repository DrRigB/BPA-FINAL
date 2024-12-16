# tracker/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

EXERCISE_CATEGORIES = [
    ('cardio', 'Cardio'),
    ('weightlifting', 'Weightlifting'),
]

CARDIO_TYPES = [
    ('running', 'Running'),
    ('cycling', 'Cycling'),
    ('swimming', 'Swimming'),
    ('walking', 'Walking'),
    ('hiit', 'HIIT'),
]

WEIGHTLIFTING_TYPES = [
    ('chest', 'Chest'),
    ('back', 'Back'),
    ('legs', 'Legs'),
    ('shoulders', 'Shoulders'),
    ('arms', 'Arms'),
    ('core', 'Core'),
]

class Activity(models.Model):
    name = models.CharField(max_length=255, default="Exercise")
    duration_minutes = models.IntegerField(
        help_text="Duration of the activity in minutes",
        validators=[
            MinValueValidator(1, message="Duration must be at least 1 minute"),
            MaxValueValidator(300, message="Please limit exercise to 5 hours per session")
        ]
    )
    heart_rate = models.IntegerField(
        help_text="Average heart rate during the exercise",
        validators=[
            MinValueValidator(40, message="Heart rate seems too low"),
            MaxValueValidator(220, message="Heart rate seems too high")
        ]
    )
    calories_burned = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def calculate_calories_burned(self):
        factor = 0.063
        self.calories_burned = int(self.duration_minutes * self.heart_rate * factor)
        return self.calories_burned

    def save(self, *args, **kwargs):
        self.calculate_calories_burned()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.date}"
