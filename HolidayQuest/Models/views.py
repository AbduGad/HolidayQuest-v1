from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import Hotel, Country, City
from .serializers import HotelSerializer, CountrySerializer, CitySerializer
from HolidayQuest.forms import HotelForm
import requests

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
@api_view(['POST'])
@permission_classes([AllowAny])
def create_hotel(request):
    print("FILES:", request.FILES)
    print("POST:", request.POST)

    # Combine the data
    data = request.POST.dict()
    if request.FILES.get('image'):
        data['image'] = request.FILES['image']

    hotel_serializer = HotelSerializer(data=data)

    if hotel_serializer.is_valid():
        hotel_serializer.save()
        return Response(hotel_serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Error in serializer:", hotel_serializer.errors)
        return Response(hotel_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow overriding via query parameters
    max_page_size = 100  # Maximum items per page


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
