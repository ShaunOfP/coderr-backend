from rest_framework import serializers
from userauth_app.models import CustomUser

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id')
    
    class Meta:
        model = CustomUser
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 
                  'location', 'tel', 'description', 'working_hours', 
                  'type', 'email', 'created_at']
        read_only_fields = ['user', 'created_at', 'type']


class BusinessProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id')

    class Meta:
        model = CustomUser
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 
                  'location', 'tel', 'description', 'working_hours', 
                  'type']


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id')

    class Meta:
        model = CustomUser
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'uploaded_at', 'type']