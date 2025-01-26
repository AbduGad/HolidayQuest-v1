import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class HomePage(APIView):
    """
    Home page
    """
    permission_classes = [AllowAny]

    def get(self, request):

        return render(request, 'home.html')
