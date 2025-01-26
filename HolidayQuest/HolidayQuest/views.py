import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from Models.models import Hotel


class HomePage(APIView):
    """
    Home page
    """
    permission_classes = [AllowAny]

    def get(self, request):

        return render(request, 'home.html')

class hotel_listing_page(APIView):
    """
    Hotel listing page
    """
    permission_classes=[AllowAny]
    
    def get(self, request):
        
        return render(request, 'hotel-listing.html')

class user_hotel_listing_page(APIView):
    """
    User hotel listing page
    """
    permission_classes=[AllowAny]
    
    def get(self, request):
        user_id = request.user.id
        hotels = Hotel.objects.filter(created_by=user_id)
        
        return render(request, 'user-hotel-listing.html', {'hotels': hotels, 
                                                           'username': request.user.first_name})
    
    