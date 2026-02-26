from django.db import models
from django.contrib.auth.models import User as AuthUser

ROLE_CHOICES = (
    ('jobseeker', 'Job Seeker'),
    ('recruiter', 'Recruiter'),
)

GENDER_CHOICES = (  # Capitalized for consistency
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)

# User model with a OneToOneField
class User(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='jobseeker')
    email=models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')

    #personal details
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    #contact details
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    #resume
    resume = models.FileField(upload_to='resumes/', blank=True)
    skills = models.TextField(blank=True)
    languages = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    hobbies = models.TextField(blank=True)
    # work 
    work_experience = models.TextField(blank=True)
    work_history = models.TextField(blank=True)
    # education
    education = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    internships= models.TextField(blank=True)
    # link
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.user.username}'s Job Seeker Profile"

class RecruiterProfile(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    profile_picture= models.ImageField(upload_to='profile_pictures/', blank=True)

    #details
    experience = models.TextField(blank=True)
    company_position= models.CharField(max_length=200, blank=True)

    #company
    company_logo = models.ImageField(upload_to='company_logos/', blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    company_website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)
    company_address = models.TextField(blank=True)
    company_phone = models.CharField(max_length=20, blank=True)
    company_email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.user_profile.user.username}'s Recruiter Profile"
