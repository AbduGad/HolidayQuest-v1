from rest_framework import serializers
from .models import Hotel

class HotelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            'id', 
            'name', 
            'description', 
            'price', 
            'image', 
            'city', 
            'country'
        ]