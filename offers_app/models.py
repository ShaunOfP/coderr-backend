from django.db import models
from userauth_app.models import CustomUser


class Offer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(
        upload_to='offer-pictures/', blank=True, default="")
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.PositiveIntegerField()
    min_delivery_time = models.PositiveIntegerField()
