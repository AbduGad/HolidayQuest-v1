from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError
from rest_framework.response import Response


class User_serializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    # stops the password from appearing in the http response
    password = serializers.CharField(write_only=True)
    business = serializers.BooleanField(default=False)


    class Meta:
        """
        Meta class for User_serializer to define its model and fields that it will work on
        """
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'business']

    def create(self, validated_data):
        """
        Use the custom UserManager to create a user.
        """
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = validated_data.get('password')
        isbusiness = validated_data.get('business', False)

        if not first_name or not last_name or not email or not password:
            raise serializers.ValidationError("All fields are requiredd.")

        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            business_account=isbusiness
        )
