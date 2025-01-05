from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import User_serializer
from rest_framework.permissions import AllowAny, IsAdminUser
from.models import User


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
        email = request.data['email']
        
        if '@' not in email:
            raise ValidationError({'error': ['email must contain @ ']})
        
        serializer = User_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class login_view(APIView):
    """
    API endpoint that allows users to login.
    """
    # Allows any user to access this api
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        
        if not email or not password:
            raise AuthenticationFailed('Email and password are required.')
        
        if user is None:
            raise AuthenticationFailed('User not found. (wrong email)')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password.')
        
        # creates a tokenpair for user(accesstoken, refreshtoken)
        refresh_token = RefreshToken.for_user(user)
        
        response = Response()
        response.data = {
            'message': 'Login successful.',
            'access': str(refresh_token.access_token),  # Short-lived access token
            'refresh': str(refresh_token),  # Long-lived refresh token
        }
        response.set_cookie(key='jwt', value=refresh_token, httponly=True)
        
        return response
    
# class CreateSuperuserView(APIView):
#     """
#     API endpoint to create a superuser.
#     Only accessible by an admin user.
#     """
#     permission_classes = [IsAdminUser]

#     def post(self, request):
#         email = request.data.get('email')
#         first_name = request.data.get('first_name')
#         last_name = request.data.get('last_name')
#         password = request.data.get('password')

#         # Validate required fields
#         if not all([email, first_name, last_name, password]):
#             raise ValidationError("All fields (email, first_name, last_name, password) are required.")

#         # Check if user already exists
#         if User.objects.filter(email=email).exists():
#             raise ValidationError("A user with this email already exists.")

#         # Create the superuser
#         user = User.objects.create_superuser(
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             password=password
#         )

#         return Response({
#             "message": "Superuser created successfully.",
#             "user": {
#                 "email": user.email,
#                 "first_name": user.first_name,
#                 "last_name": user.last_name
#             }
#         })
