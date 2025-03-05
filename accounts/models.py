from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
import string

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

class VerificationCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    @classmethod
    def generate_code(cls, user):
        # Generate a random 6-digit code
        code = ''.join(random.choices(string.digits, k=6))
        # Set expiration to 15 minutes from now
        expires_at = timezone.now() + timezone.timedelta(minutes=15)
        # Create and return the verification code
        return cls.objects.create(
            user=user,
            code=code,
            expires_at=expires_at
        )

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

    class Meta:
        ordering = ['-created_at']

class Team(models.Model):
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=6, unique=True)
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='led_teams')
    members = models.ManyToManyField(CustomUser, through='TeamMembership', related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class TeamMembership(models.Model):
    ROLE_CHOICES = [
        ('LEADER', 'Team Leader'),
        ('MEMBER', 'Team Member'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'team')
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.username} - {self.team.name} ({self.role})"
