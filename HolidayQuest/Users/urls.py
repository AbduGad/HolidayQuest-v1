from django.urls import path
from .views import register_view


urlpatterns = [
    path('register/', register_view.as_view(), name='register'),
]
