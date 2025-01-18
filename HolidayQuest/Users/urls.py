from django.urls import path
from .views import LoginView, LogoutView, RegisterView, CheckAuthView, ProtectedView, UserHotelsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('isloggedin/', CheckAuthView.as_view()),
    path('protectedviewtest/', ProtectedView.as_view()),
    path(
        'user_created_hotels/',
        UserHotelsView.as_view(),
        name='user_created_hotels'),
]
