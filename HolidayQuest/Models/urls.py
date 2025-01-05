from django.urls import path
from . import views
from django.conf.urls.static import static

from django.conf import settings

urlpatterns = [
    path('create-hotel/', views.create_hotel, name='create_hotel'),
    path('get-hotels/', views.get_hotels, name='get_hotels'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
