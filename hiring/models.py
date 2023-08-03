# hiring/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add custom fields to the AbstractUser model
    # You can also modify existing fields if needed
    # username, email, and password fields are already available in AbstractUser
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
    )

class Job(models.Model):
    id = models.TextField(primary_key=True)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    skills = models.TextField()  # Storing skills as a comma-separated list (e.g., "Python,JavaScript,Django")
    description = models.TextField()

    def __str__(self):
        return self.title
    
class JobApplication(models.Model):
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Foreign key to User model for candidate's username and email
    job = models.ForeignKey(Job, on_delete=models.CASCADE)  # Foreign key to Job model
    name = models.CharField(max_length=100)  # Candidate's name
    email = models.EmailField()  # Candidate's email
    skills = models.TextField()  # Set of skills candidate is having as CSV
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # Link to resume (optional)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)  # Link to CV (optional)
    application_date = models.DateTimeField(auto_now_add=True)  # Autogenerate application date as today's date