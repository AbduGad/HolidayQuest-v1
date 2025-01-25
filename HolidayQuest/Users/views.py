from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import User_serializer
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from Users.authentication import CookieJWTAuthentication


class RegisterView(APIView):
    """
    API endpoint that allows users to be created.
    """
    # Allows any user to access this api
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Serves the registration HTML template.
        """
        return render(request, 'users/register.html')

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


class LoginView(APIView):
    """
    API endpoint that allows users to login.
    """
    # Allows any user to access this api
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Serves the login HTML template
        """
        return render(request, 'users/login.html')

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
        access_token = str(refresh_token.access_token)

        response = Response()

        response.data = {
            'message': 'Login successful.',
            'access': str(access_token),
            'refresh': str(refresh_token),
        }
        response.set_cookie(
            key='access',
            value=access_token,
            httponly=True,
            # domain='localhost',   # Shared domain for local dev
            # secure=False,         # Local development (HTTPS not required)
            # samesite=None,       # Allow cross-origin requests
            # # samesite='Lax',
            # # secure=settings.DEBUG is False,  # True in production
            max_age=3600 * 24,  # 24 hours
            # path='/'
        )

        response.set_cookie(
            key='refresh',
            value=str(refresh_token),
            httponly=True,
            # samesite='Lax',
            max_age=3600 * 24 * 7,  # 7 days
            path='/'
        )

        return response


class LogoutView(APIView):
    """
    API endpoint to log out a user by deleting the JWT cookie.
    """
    # Only authenticated users can access this endpoint
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Logout successful."})
        # Delete the JWT cookie
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response

    def get(self, request):
        response = redirect('login')
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        messages.success(request, 'Logged out successfully.')
        return response


class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"authenticated": True})


# @method_decorator(csrf_exempt, name='dispatch')
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        return Response({
            'message': 'You have access to this protected resource'
        })

# http://127.0.0.1:8000/user/user_created_hotels/


class UserHotelsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        # Fetch the hotels associated with the authenticated user
        user: User = request.user
        hotels = user.hotels.all()  # Assuming `hotels` is a related name
        print(hotels)
        # Convert the hotel objects to a dictionary or serialize them
        hotels_data = [
            {
                'id': hotel.id,
                'name': hotel.name,
            } for hotel in hotels
        ]

        return Response({'hotels': hotels_data})
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
