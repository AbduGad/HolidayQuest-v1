from django.urls import path
from . import views
from django.conf.urls.static import static

from django.conf import settings

urlpatterns = [
    path('create-hotel/', views.create_hotel, name='create_hotel'),
    path('get-hotels/', views.get_hotels, name='get_hotels'),
    path('get-hotel/', views.get_hotel_detail, name='get-hotel')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Get by ID
# GET /api/hotel/?id=1
# Get by name
# GET /api/hotel/?name=Amon hotel
