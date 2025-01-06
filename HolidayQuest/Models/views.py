from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import Hotel, Country, City
from .serializers import HotelSerializer, CountrySerializer, CitySerializer
from HolidayQuest.forms import HotelForm
import requests
from django.shortcuts import get_object_or_404
# Allow anyone to access this view


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def create_hotel(request):
#     hotel_serializer = HotelSerializer(data=request.data)
#     # print(
#     #     "image empty?",
#     #     hotel_serializer.is_valid(),
#     #     not request.data.get("image"))

#     if hotel_serializer.is_valid():
#         hotel_serializer.save()
#         return Response(hotel_serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         # Log or print the errors for debugging
#         print("Error in serializer:", hotel_serializer.errors)  # Log the errors
#         return Response(hotel_serializer.errors,
#                         status=status.HTTP_400_BAD_REQUEST)
######################
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def create_hotel(request):
#     # Combine request.data and request.FILES
#     data = request.data.copy()
#     data.update(request.FILES)

#     hotel_serializer = HotelSerializer(data=data)

#     print("Files:", request.FILES)  # Debug print
#     print("Data:", data)  # Debug print

#     if hotel_serializer.is_valid():
#         hotel_serializer.save()
#         return Response(hotel_serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         print("Error in serializer:", hotel_serializer.errors)
#         return Response(hotel_serializer.errors,
#                         status=status.HTTP_400_BAD_REQUEST)

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
