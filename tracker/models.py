from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.core.cache import cache

class Activity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name='User'
    )
    name = models.CharField(max_length=255, default="Exercise", db_index=True)
    duration_minutes = models.IntegerField(
        help_text="Duration of the activity in minutes",
        validators=[
            MinValueValidator(1, message="N/A, please try again"),
            MaxValueValidator(300, message="Please limit exercise to 5 hours per session")
        ]
    )
    heart_rate = models.IntegerField(
        help_text="Average heart rate during the exercise",
        validators=[
            MinValueValidator(40, message="N/A, please try again"),
            MaxValueValidator(220, message="N/A, please try again")
        ]
    )
    calories_burned = models.IntegerField(
        blank=True, 
        null=True, 
        db_index=True,
        validators=[
            MinValueValidator(0, message="Calories burned cannot be negative"),
            MaxValueValidator(5000, message="Calories burned seems too high")
        ]
    )
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['date', 'name']),
            models.Index(fields=['calories_burned', 'date']),
            models.Index(fields=['user', 'date']),
        ]
        ordering = ['-date']
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def calculate_calories_burned(self):
        cache_key = f'calories_burned_{self.id}'
        cached_value = cache.get(cache_key)
        
        if cached_value is not None:
            return cached_value
            
        factor = 0.063
        calories = int(self.duration_minutes * self.heart_rate * factor)
        cache.set(cache_key, calories, timeout=3600)
        return calories

    def save(self, *args, **kwargs):
        if not self.calories_burned:
            self.calories_burned = self.calculate_calories_burned()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} by {self.user.username} on {self.date.strftime('%Y-%m-%d %H:%M')}"

