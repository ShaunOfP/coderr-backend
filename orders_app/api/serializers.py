from rest_framework import serializers

from orders_app.models import Order
from offers_app.models import OfferDetail


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializes the fields for the /api/orders/ endpoint when using the POST-Method"""
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['offer_detail_id', 'id']
        read_only_fields = ['id']
        write_only_fields = ['offer_detail_id']

    def create(self, validated_data):
        """Validates if a user is of type business and assigns the matching offer data to the order"""
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
    """
    Serializes the fields for the endpoint /api/orders/ when using the GET-Method 
    and for the endpoint /api/orders/{id}/ when using DELETE or PATCH
    """
    class Meta:
        model = Order
        fields = ["id", "customer_user", "business_user", "title", "revisions", "delivery_time_in_days",
                  "price", "features", "offer_type", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "customer_user", "business_user", "title", "revisions", "delivery_time_in_days",
                            "price", "features", "offer_type", "created_at", "updated_at"]


class OrderCountSerializer(serializers.ModelSerializer):
    """Serializes the field for the /api/order-count/{business_user_id}/ endpoint"""
    order_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_count']

    def get_order_count(self, obj):
        """Retrieves the count of orders for the given business user"""
        return Order.objects.filter(business_user=obj, status='in_progress').count()


class CompletedOrderCountSerializer(serializers.ModelSerializer):
    """Serializes the field for the /api/completed-order-count/{business_user_id}/ endpoint"""
    completed_order_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['completed_order_count']

    def get_completed_order_count(self, obj):
        """Retrieves the count of completed orders for the given business user"""
        return Order.objects.filter(business_user=obj, status='completed').count()
