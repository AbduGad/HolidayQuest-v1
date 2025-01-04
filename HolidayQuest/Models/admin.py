from django.contrib import admin
from .models import Country, City, Hotel


class HotelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'city',
        'country',
        'price',
        'rooms_available',
        'total_rooms',
        'created_at',
        'updated_at')
    search_fields = ('name', 'address', 'city__name', 'country__name')
    list_filter = ('country', 'city')


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_at', 'updated_at')
    search_fields = ('name', 'country__name')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


# Registering models with the admin
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Hotel, HotelAdmin)
