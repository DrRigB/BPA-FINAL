from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add any additional fields you want here
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.username
