from rest_framework import serializers
from .models import User


class User_serializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        
    def create(self, validated_data):
        """
        Use the custom UserManager to create a user.
        """
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')  # Make sure this is accessed safely
        email = validated_data.get('email')
        password = validated_data.get('password')

        if not first_name or not last_name or not email or not password:
            raise serializers.ValidationError("All fields are required.")
        
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        