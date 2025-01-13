from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


class CookieJWTAuthentication(JWTAuthentication):
    '''
    Custom JWT authentication class that uses cookies instead of headers.
    '''

    def authenticate(self, request):
        '''
        Authenticate the user based on the JWT token in the cookie.
        '''
        access_token = request.COOKIES.get('access')

        if not access_token:
            # If no token in cookie, check the Authorization header
            auth_header = request.headers.get('Authorization')

            if auth_header:
                parts = auth_header.split()
                if len(parts) == 2 and parts[0].lower() == 'bearer':
                    access_token = parts[1]

        if not access_token:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except InvalidToken:
            raise AuthenticationFailed('Invalid token or token has expired')


# from rest_framework.authentication import BaseAuthentication
# from django.conf import settings
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.models import User
# import jwt
# class CookieJWTAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         # Get the refresh token from cookies
#         refresh_token = request.COOKIES.get('refresh_token')

#         if not refresh_token:
#             raise AuthenticationFailed('Refresh token not found in cookies.')

#         try:
#             # Decodes the refresh token (verify it's a valid token)
#             token = RefreshToken(refresh_token)

#             # Uses the token to get the user from the payload
#             user_id = token['user_id']
#             user = User.objects.filter(id=user_id).first()

#             if user is None:
#                 raise AuthenticationFailed('User not found.')

#             # issue a new access token
#             access_token = str(token.access_token)

#         except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
#             raise AuthenticationFailed(f'Token error: {str(e)}')

#         # access token in request for possible use in views
#         request.access_token = access_token
#         return (user, None)
