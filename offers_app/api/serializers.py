from rest_framework import serializers
from rest_framework.reverse import reverse

from offers_app.models import Offer, OfferDetail
from userauth_app.models import CustomUser


class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializes the fields for the /api/offerdetails/ endpoint"""
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['id', 'revisions']


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializes the fields for the POST-Method on the endpoint /api/offers/
    Modifies the create function
    """
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
    """Serializes the HyperLinked url in a shortened form"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        extra_kwargs = {
            'url': {'view_name': 'offer-detail', 'lookup_field': 'pk'}
        }

    def get_url(self, obj):
        """Removes /api from the Hyperlink to create a short form"""
        url = reverse('offer-detail', kwargs={'pk': obj.pk})
        return url.replace('/api', '')


class OfferGetSerializer(serializers.ModelSerializer):
    """Serializes the fields for the /api/offers/ endpoint when using the GET-Method"""
    user = serializers.PrimaryKeyRelatedField(source='creator', read_only=True)
    details = DetailsHyperLinkedSerializer(
        many=True, read_only=True)
    user_details = UserDetailsSerializer(source='creator', read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at',
                  'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']


class DetailsLongHyperLinkedSerializer(serializers.HyperlinkedModelSerializer):
    """Serializes the HyperLinked url for the OfferDetails"""
    url = serializers.HyperlinkedIdentityField(
        view_name='offer-detail',
        lookup_field='pk'
    )

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        extra_kwargs = {
            'url': {'view_name': 'offer-detail', 'lookup_field': 'pk'}
        }


class OfferSingleSerializer(serializers.ModelSerializer):
    """Serializes the fields for the /api/offers/{id}/ endpoint"""
    user = serializers.PrimaryKeyRelatedField(source='creator', read_only=True)
    details = DetailsLongHyperLinkedSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at',
                  'updated_at', 'details', 'min_price', 'min_delivery_time']


class OfferPatchSerializer(serializers.ModelSerializer):
    """Serializes the fields for the /api/offers/{id}/ endpoint when using the PATCH-Method"""
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        """Makes sure that the validated_data['details'] are patched at the correct spot"""
        details_data = validated_data.pop('details', [])

        instance = super().update(instance, validated_data)

        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            try:
                detail_instance = instance.details.get(offer_type=offer_type)
            except OfferDetail.DoesNotExist:
                raise serializers.ValidationError(
                    {'error': 'Invalid request data'})

            for attr, value in detail_data.items():
                setattr(detail_instance, attr, value)
            detail_instance.save()
        return instance
