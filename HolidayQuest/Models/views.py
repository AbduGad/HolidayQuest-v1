from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import Hotel, Country, City
from .serializers import EditHotelSerializer, HotelSerializer, CountrySerializer, CitySerializer
from HolidayQuest.forms import HotelForm
import requests
from django.shortcuts import get_object_or_404
# Allow anyone to access this view
from django.http import JsonResponse

# http://127.0.0.1:8000/api/create-hotel/


@api_view(['POST'])
@permission_classes([AllowAny])
def create_hotel(request):

    # Combine the data
    data = request.POST.dict()
    if request.FILES.get('image'):
        data['image'] = request.FILES['image']

    hotel_serializer = HotelSerializer(data=data)

    if hotel_serializer.is_valid():
        hotel_serializer.save()
        return Response(hotel_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(hotel_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow overriding via query parameters
    max_page_size = 100  # Maximum items per page

# http://localhost:8000/api/get-hotels/


@api_view(['GET'])
@permission_classes([AllowAny])
def get_hotels(request):
    # Query all hotels
    hotels = Hotel.objects.all()

    # Apply pagination
    paginator = CustomPagination()
    paginated_hotels = paginator.paginate_queryset(hotels, request)

    # Serialize the paginated data
    hotel_serializer = HotelSerializer(
        paginated_hotels, many=True, context={
            'request': request})

    # Return paginated response
    return paginator.get_paginated_response(hotel_serializer.data)

# http://localhost:8000/api/get-hotel/?id=1
# http://localhost:8000/api/get-hotel/?name=four%20seasons


@api_view(['GET'])
@permission_classes([AllowAny])
def get_hotel_detail(request):
    hotel_id = request.query_params.get('id')
    hotel_name = request.query_params.get('name')

    try:
        if hotel_id:
            hotel = get_object_or_404(Hotel, id=hotel_id)
        elif hotel_name:
            hotel = get_object_or_404(Hotel, name__iexact=hotel_name)
        else:
            return Response(
                {"error": "Please provide either hotel id or name"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = HotelSerializer(hotel, context={'request': request})
        return Response(serializer.data)

    except Hotel.DoesNotExist:
        return Response(
            {"error": "Hotel not found"},
            status=status.HTTP_404_NOT_FOUND
        )

# http://127.0.0.1:8000/api/hotels/search?country=Jordan

# http://127.0.0.1:8000/api/hotels/search?country=Egypt&city=luxor&min_price=50&max_price=600


@api_view(['GET'])
@permission_classes([AllowAny])
def get_hotels_by_location(request):
    country = request.query_params.get('country')
    city = request.query_params.get('city')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    if not any([country, city, min_price, max_price]):
        return Response(
            {
                "error": "Please provide at least one search criteria (country, city, or price range)."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        queryset = Hotel.objects.all()

        if country:
            queryset = queryset.filter(country__name__iexact=country)

        if city:
            queryset = queryset.filter(city__name__iexact=city)

        # Add price range filtering
        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                return Response(
                    {"error": "Invalid minimum price value."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                return Response(
                    {"error": "Invalid maximum price value."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if not queryset.exists():
            return Response(
                {"error": "No hotels found for the given criteria."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = HotelSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
# http://127.0.0.1:8000/api/edit-hotel/?name=15%20seasons
# 'http://127.0.0.1:8000/api/edit-hotel/?hotel_id=1'


@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_hotel(request):
    # Get hotel ID and name from query parameters
    hotel_id = request.GET.get('hotel_id')
    hotel_name = request.GET.get('hotel_name')

    if not hotel_id and not hotel_name:
        return JsonResponse({"detail": "Hotel ID or name is required."},
                            status=status.HTTP_400_BAD_REQUEST)

    try:
        if hotel_id:
            # Fetch the hotel object by ID
            hotel = Hotel.objects.get(id=hotel_id)
        elif hotel_name:
            # Fetch the hotel object by name
            hotel = Hotel.objects.get(name=hotel_name)
    except Hotel.DoesNotExist:
        return JsonResponse({"detail": "Hotel not found."},
                            status=status.HTTP_404_NOT_FOUND)

    # Prepare the data
    data = request.data.copy()
    if request.FILES.get('image'):
        data['image'] = request.FILES['image']

    hotel_serializer = EditHotelSerializer(hotel, data=data, partial=True)
    if hotel_serializer.is_valid():
        hotel_serializer.save()
        return JsonResponse(hotel_serializer.data, status=status.HTTP_200_OK)
    else:
        return JsonResponse(hotel_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# http://127.0.0.1:8000/api/delete-hotel/?id=0
# http://127.0.0.1:8000/api/delete-hotel/?name=15%20seasons
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_hotel(request):
    # Get hotel ID and name from query parameters
    hotel_id = request.query_params.get('id')
    hotel_name = request.query_params.get('name')

    if not hotel_id and not hotel_name:
        return Response({'error': 'Hotel ID or name is required'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        if hotel_id:
            # Fetch the hotel object by ID
            hotel = Hotel.objects.get(id=hotel_id)
        elif hotel_name:
            # Fetch the hotel object by name
            hotel = Hotel.objects.get(name=hotel_name)

        hotel.delete()  # Delete the hotel from the database
        return Response({'message': 'Hotel deleted successfully'},
                        status=status.HTTP_204_NO_CONTENT)
    except Hotel.DoesNotExist:
        return Response({'error': 'Hotel not found'},
                        status=status.HTTP_404_NOT_FOUND)
