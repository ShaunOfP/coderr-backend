from rest_framework import serializers

from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializes the fields for the endpoint /api/reviews/ and /api/reviews/{id}/"""
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'reviewer']

    def validate(self, attrs):
        """Validates rating to only allow values between 1 and 5"""
        if attrs['rating'] not in [1, 2, 3, 4, 5]:
            raise serializers.ValidationError(
                {'error': 'Ratings are only possible between 1 to 5'})
        return super().validate(attrs)

    def create(self, validated_data):
        """
        Checks if the given business_user is of type business. Raises error if not.
        Assigns the authenticated user as reviewer when creating a new review.
        """
        if validated_data['business_user'].type != 'business':
            raise serializers.ValidationError(
                {'error': 'Selected user is not a business user'})

        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)
