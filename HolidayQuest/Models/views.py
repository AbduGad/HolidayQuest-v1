from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Country, City, Hotel
from .serializers import HotelSerializer, CountrySerializer, CitySerializer


@api_view(['POST'])
def create_hotel(request):

    hotel_serializer = HotelSerializer(data=request.data)

    if hotel_serializer.is_valid():
        hotel_serializer.save()
        return Response(hotel_serializer.data,
                        status=status.HTTP_201_CREATED)
    else:
        return Response(hotel_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
