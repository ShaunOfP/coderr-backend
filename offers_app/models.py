from django.db import models

from userauth_app.models import CustomUser


class OfferDetail(models.Model):
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField(default=0)
    price = models.FloatField()
    features = models.JSONField()
    offer_type = models.CharField(max_length=255)
    offer = models.ForeignKey(
        'Offer', on_delete=models.CASCADE, related_name='details')


class Offer(models.Model):
    creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='offer_creator')
    title = models.CharField(max_length=255)
    image = models.FileField(
        upload_to='offer-pictures/', blank=True, null=True, default="")
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.FloatField(default=0)
    min_delivery_time = models.PositiveIntegerField(default=0)
