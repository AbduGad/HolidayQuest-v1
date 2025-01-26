from django.urls import path
from . import views
from django.conf.urls.static import static

from django.conf import settings
app_name = 'Api_forms'


urlpatterns = [
    path(
        'hotel/edit/',
        views.hotel_management,
        name='edit_hotel'
    ),
    path('create-hotel/', views.create_hotel_form, name='create_hotel'),

]
