from django.db import models
from django.contrib.auth.models import User

Gender_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, default='')
    gender = models.CharField(max_length=10, choices=Gender_CHOICES, default='male')

    def __str__(self):
        return self.user.username


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, default='')
    gender = models.CharField(max_length=10, choices=Gender_CHOICES, default='male')

    def __str__(self):
        return self.user.username
