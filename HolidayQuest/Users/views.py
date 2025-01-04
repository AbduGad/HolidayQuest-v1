from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .serializer import User_serializer
from rest_framework.permissions import AllowAny


class register_view(APIView):
    """
    API endpoint that allows users to be created.
    """
    # Allows any user to access this api
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Creates the new user. POST request
        """
        if '@' not in request.data['email']:
            raise ValidationError({'error': ['email must contain @ ']})
        serializer = User_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

        