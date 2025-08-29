from django.db import models

from userauth_app.models import CustomUser
from offers_app.models import Offer


class Order(models.Model):
    customer_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='order_customer')
    business_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='order_business')
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    features = models.JSONField()
    offer_type = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
