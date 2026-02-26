from django.db import models

class Job(models.Model):

    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]

    JOB_CATEGORIES = [
        ('it', 'IT / Software'),
        ('marketing', 'Marketing'),
        ('finance', 'Finance'),
        ('hr', 'Human Resources'),
        ('other', 'Other'),
    ]

    recruiter = models.ForeignKey(
        'accounts.RecruiterProfile',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPES
    )

    job_category = models.CharField(
        max_length=50,
        choices=JOB_CATEGORIES
    )

    job_description = models.TextField()

    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    salary = models.DecimalField(max_digits=10, decimal_places=2)

    education_requirements = models.TextField()
    experience_requirements = models.TextField()
    skills_required = models.TextField()
    languages_required = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.company}"