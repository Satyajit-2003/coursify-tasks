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


    # Example of adding a new field
    phone_number = models.CharField(max_length=15, blank=True)

    # Add more fields as needed

class Job(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    skills = models.TextField()  # Storing skills as a comma-separated list (e.g., "Python,JavaScript,Django")
    description = models.TextField()

    def __str__(self):
        return self.title