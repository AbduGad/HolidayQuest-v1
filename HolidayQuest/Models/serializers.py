from rest_framework import serializers
from .models import Country, City, Hotel
from rest_framework.exceptions import ValidationError
from django.db.models import Q


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    country = serializers.CharField(write_only=True, required=True)
    city = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Hotel
        fields = [  # Include all fields except 'country' and 'city'
            'id', 'name', 'address', 'rooms_available', 'total_rooms',
            'price', 'description', 'country', 'city'
        ]

    def validate(self, data):
        # Extract the name, address, country_name, and city_name from the
        # validated data

        hotel_name = data.get('name')
        address = data.get('address')
        country_name = data.get('country')
        city_name = data.get('city')

        # Check if required fields are missing
        if not country_name:
            raise ValidationError(
                {'country': "Country name is required."})
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

        # check if there is a hotel with same name exists
        if Hotel.objects.filter(country=country, city=city,
                                name=hotel_name).exists():
            raise ValidationError({
                'non_field_errors': "A hotel with the same name already exists"
            })

        # check if there is a hotel with same address exists
        if Hotel.objects.filter(
                country=country, city=city, address=address).exists():
            raise ValidationError({
                'non_field_errors': "A hotel with the same address already exists"
            })

        # Return the validated data if no validation errors occurred
        return data

    def create(self, validated_data):
        # Extract country and city from validated_data
        country = validated_data.pop('country')
        city = validated_data.pop('city')

        # Create the hotel instance with the foreign keys
        hotel = Hotel.objects.create(
            country=country, city=city, **validated_data)
        return hotel
