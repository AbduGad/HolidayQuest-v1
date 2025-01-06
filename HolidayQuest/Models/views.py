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


# http://127.0.0.1:8000/api/edit-hotel/
@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_hotel(request):
    hotel_id = request.GET.get('hotel_id')
    if not hotel_id:
        return JsonResponse({"detail": "Hotel ID is required."},
                            status=status.HTTP_400_BAD_REQUEST)

    try:
        hotel = Hotel.objects.get(id=hotel_id)
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

# http://127.0.0.1:8000/api/Delete-hotel/


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_hotel(request):
    # Get hotel ID from query parameters
    hotel_id = request.query_params.get('id')

    if not hotel_id:
        return Response({'error': 'Hotel ID is required'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the hotel object by ID
        hotel = Hotel.objects.get(id=hotel_id)
        hotel.delete()  # Delete the hotel from the database
        return Response({'message': 'Hotel deleted successfully'},
                        status=status.HTTP_204_NO_CONTENT)
    except Hotel.DoesNotExist:
        return Response({'error': 'Hotel not found'},
                        status=status.HTTP_404_NOT_FOUND)
