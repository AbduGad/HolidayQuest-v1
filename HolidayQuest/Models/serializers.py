from rest_framework import serializers
from .models import Country, City, Hotel
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework import serializers
from .models import Hotel, Country, City
from django.db import models
from Users.models import User
from Users.serializer import User_serializer
from django.core.exceptions import ObjectDoesNotExist


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    country = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    image = serializers.ImageField(required=True)
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    rooms_available = serializers.IntegerField()
    total_rooms = serializers.IntegerField()
    # For GET requests - returns full user representation
    # created_by = User_serializer()
    # user_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     required=True,
    #     write_only=True,
    #     source='created_by'
    # )

    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'address', 'rooms_available', 'total_rooms',
            'price', 'description', 'country', 'city', 'image',
            # "user_id"
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        hotel = Hotel.objects.create(
            created_by=user,
            **validated_data
        )
        return hotel

    def validate(self, data):
        hotel_name = data.get('name')
        address = data.get('address')
        country_name = data.get('country')
        city_name = data.get('city')

        # Check if required fields are missing
        if not country_name:
            raise ValidationError({'country': "Country name is required."})
        if not city_name:
            raise ValidationError({'city': "City name is required."})
        if not hotel_name:
            raise ValidationError({'name': "Hotel name is required."})
        if not address:
            raise ValidationError({'address': "Address is required."})

        # Retrieve or create the Country and City instances
        country, _ = Country.objects.get_or_create(name=country_name)
        city, _ = City.objects.get_or_create(name=city_name, country=country)

        # Add the actual country and city objects to the validated data
        data['country'] = country
        data['city'] = city

        # Check if there is a hotel with the same name
        if Hotel.objects.filter(country=country, city=city,
                                name=hotel_name).exists():
            raise ValidationError(
                {'non_field_errors': "A hotel with the same name already exists"})

        # Check if there is a hotel with the same address
        if Hotel.objects.filter(country=country, city=city,
                                address=address).exists():
            raise ValidationError(
                {'non_field_errors': "A hotel with the same address already exists"})

        return data


class EditHotelSerializer(serializers.ModelSerializer):
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)

    class Meta:
        model = Hotel
        fields = [
            'name', 'address', 'rooms_available', 'total_rooms',
            'price', 'description', 'country', 'city', 'image'
        ]

    def validate(self, data):
        # Retrieve the instance being updated
        hotel_instance = self.instance

        # Use the provided country and city, or fall back to the instance's
        # values
        country_name = data.get('country') or (
            hotel_instance.country.name if hotel_instance else None)
        city_name = data.get('city') or (
            hotel_instance.city.name if hotel_instance else None)

        if not country_name:
            raise serializers.ValidationError(
                {'country': "Country name is required for updates."})
        if not city_name:
            raise serializers.ValidationError(
                {'city': "City name is required for updates."})

        # Retrieve or create the Country and City instances
        country, _ = Country.objects.get_or_create(name=country_name)
        city, _ = City.objects.get_or_create(name=city_name, country=country)

        # Add the actual country and city objects to the validated data
        data['country'] = country
        data['city'] = city

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        hotel = Hotel.objects.create(
            created_by=user,
            **validated_data
        )
        return hotel

    def update(self, instance, validated_data):
        # Handle country and city updates
        country = validated_data.pop('country', instance.country)
        city = validated_data.pop('city', instance.city)

        # Update the instance fields
        instance.country = country
        instance.city = city
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
