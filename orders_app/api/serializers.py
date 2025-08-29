from rest_framework import serializers

from orders_app.models import Order
from offers_app.models import OfferDetail


class OrderCreateSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['offer_detail_id', 'id']
        read_only_fields = ['id']
        write_only_fields = ['offer_detail_id']

    def create(self, validated_data):
        request = self.context['request']
        customer_user = request.user

        offer_detail_id = validated_data.pop('offer_detail_id')
        try:
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError(
                {'error': 'Invalid request data'})

        business_user = offer_detail.offer.creator

        order = Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type
        )

        return order


class OrderResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "customer_user", "business_user", "title", "revisions", "delivery_time_in_days",
                  "price", "features", "offer_type", "status", "created_at", "updated_at"]
