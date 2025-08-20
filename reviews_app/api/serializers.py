from rest_framework import serializers, status

from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'reviewer']

    def validate(self, data):
        """Validates if the given business_user is in fact of type business"""
        if data['business_user'].type != 'business':
            raise serializers.ValidationError(
                {'error': 'Selected user is not a business user'}, status=status.HTTP_400_BAD_REQUEST)
        return data

    def create(self, validated_data):
        """Assigns the authenticated user as reviewer when creating a new review"""
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)
