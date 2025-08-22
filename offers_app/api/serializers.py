from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['id', 'revisions']


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        """
        Checks if Offer has at least 3 types of detail.
        Calculates min_price and min_delivery_time and saves it to the Offer
        """
        details_data = validated_data.pop("details", [])
        if len(details_data) < 3:
            raise serializers.ValidationError({'error': 'Offer must have at least 3 details'})
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        if details_data:
            offer.min_price = min(d["price"] for d in details_data)
            offer.min_delivery_time = min(
                d["delivery_time_in_days"] for d in details_data)
            offer.save()
        return offer
