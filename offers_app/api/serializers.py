from rest_framework import serializers
from rest_framework.reverse import reverse

from offers_app.models import Offer, OfferDetail
from userauth_app.models import CustomUser


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['id', 'revisions']


class OfferCreateSerializer(serializers.ModelSerializer):
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
            raise serializers.ValidationError(
                {'error': 'Offer must have at least 3 details'})
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        if details_data:
            offer.min_price = min(d["price"] for d in details_data)
            offer.min_delivery_time = min(
                d["delivery_time_in_days"] for d in details_data)
            offer.save()
        return offer


class UserDetailsSerializer(serializers.ModelSerializer):
    """Creates the needed details for the user on an offer when using the GET-Method on Endpoint /api/offers/"""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username']


class DetailsHyperLinkedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        extra_kwargs = {
            'url': {'view_name': 'offer-detail', 'lookup_field': 'pk'}
        }

    def get_url(self, obj):
        url = reverse('offer-detail', kwargs={'pk': obj.pk})
        return url.replace('/api', '')


class OfferGetSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='creator', read_only=True)
    details = DetailsHyperLinkedSerializer(
        many=True, read_only=True)
    user_details = UserDetailsSerializer(source='creator', read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at',
                  'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']
