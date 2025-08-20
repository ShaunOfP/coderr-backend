from rest_framework import serializers

from offers_app.models import Offer

class OfferSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at',
                  'min_price', 'min_deliver_time']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']