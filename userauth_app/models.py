from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Custom User Model which supports two different types of a user"""
    USER_TYPES = (
        ("customer", "Customer"),
        ("business", "Business")
    )

    file = models.FileField(
        upload_to='profile-pictures/', blank=True, default="")
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(max_length=255, blank=True, default="")
    working_hours = models.CharField(max_length=255, blank=True, default="")
    type = models.CharField(
        max_length=20, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
