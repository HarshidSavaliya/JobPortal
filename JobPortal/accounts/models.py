from django.db import models
from django.contrib.auth.models import User as AuthUser  # Rename to avoid conflict

ROLE_CHOICES = (
    ('jobseeker', 'Job Seeker'),
    ('recruiter', 'Recruiter'),
)

GENDER_CHOICES = (  # Capitalized for consistency
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)

# Backward-compatible alias used by existing form imports.
Gender_CHOICES = GENDER_CHOICES

# Option 1: Extend the built-in User model with a OneToOneField
class UserProfile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='jobseeker')
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')

    def __str__(self):
        return f"{self.user.username}'s profile"
