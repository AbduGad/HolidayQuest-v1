from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import requests
from django.http import JsonResponse
from Models.models import Hotel


class EditDeleteHotelForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(widget=forms.Textarea)
    rooms_available = forms.IntegerField()
    total_rooms = forms.IntegerField()
    country = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    image = forms.ImageField()


class CreateHotelForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    price = forms.FloatField()
    description = forms.CharField(widget=forms.Textarea)
    rooms_available = forms.IntegerField()
    total_rooms = forms.IntegerField()
    country = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    image = forms.ImageField(required=True)

# http://127.0.0.1:8000/Api_forms/hotel/edit/


def hotel_management(request, hotel_id=None):
    form = EditDeleteHotelForm()

    return render(request, 'Api_forms/hotel_form.html', {
                  'form': form, 'hotel_id': hotel_id})


# http://127.0.0.1:8000/Api_forms/create-hotel/


def create_hotel_form(request):
    print(request)
    if request.method == 'POST':
        form = CreateHotelForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a MultipartEncoder for proper file handling
            data = {
                'name': form.cleaned_data['name'],
                'address': form.cleaned_data['address'],
                # Convert to string
                'price': str(float(form.cleaned_data['price'])),
                'description': form.cleaned_data['description'],
                'rooms_available': str(form.cleaned_data['rooms_available']),
                'total_rooms': str(form.cleaned_data['total_rooms']),
                'country': form.cleaned_data['country'],
                'city': form.cleaned_data['city'],
            }
            # Handle the file separately
            files = {
                'image': (
                    request.FILES['image'].name,
                    request.FILES['image'],
                    request.FILES['image'].content_type
                )
            }

            # Make the request
            response = requests.post(
                "http://127.0.0.1:8000/api/create-hotel/",
                data=data,
                files=files
            )

            if response.status_code == 201:
                return render(
                    request, 'HolidayQuest/success.html', {'data': data})
            else:
                error_data = response.json()
                error_message = error_data.get(
                    'non_field_errors', ['An error occurred'])[0]
                return render(request, 'HolidayQuest/error.html',
                              {'error': error_message})
    else:
        form = CreateHotelForm()

    return render(request, 'Api_forms/create-hotel.html', {'form': form})
