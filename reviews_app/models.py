from django.db import models

from userauth_app.models import CustomUser


class Review(models.Model):
    business_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='business_reviews')
    reviewer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.PositiveSmallIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
