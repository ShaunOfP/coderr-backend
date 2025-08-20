from rest_framework import serializers
from django.contrib.auth import authenticate

from userauth_app.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        write_only_fields = ['type', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        """checks if passwords match and if mail is already in use. Sets the account details and saves afterwards"""
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError(
                {'error': 'Passwords dont match'})

        if CustomUser.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'Email already exists'})
        
        if self.validated_data['type'] not in ["business", "customer"]:
            raise serializers.ValidationError(
                {'error': 'Viable options for type are business or customer'})

        account = CustomUser(
            email=self.validated_data['email'], username=self.validated_data['username'], type=self.validated_data['type'])
        account.set_password(pw)
        account.save()
        return account


class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        """returns the user which authenticates via mail and password"""
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError('Invalid email or password')

            user = authenticate(username=user.username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password')
        else:
            raise serializers.ValidationError(
                'Must include email and password')

        attrs['user'] = user
        return attrs
