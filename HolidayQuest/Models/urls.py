from django.urls import path
from . import views


urlpatterns = [
    path('create-hotel/', views.create_hotel, name='create_hotel'),
]
