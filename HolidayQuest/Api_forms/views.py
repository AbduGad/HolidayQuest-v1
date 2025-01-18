from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
import requests


class HotelForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(widget=forms.Textarea)
    rooms_available = forms.IntegerField()
    total_rooms = forms.IntegerField()
    country = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    image = forms.ImageField()


# def hotel_management(request, hotel_id=None):
#     if request.method == 'POST':
#         form = HotelForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Prepare form data
#             data = {
#                 'name': form.cleaned_data['name'],
#                 'address': form.cleaned_data['address'],
#                 'price': str(form.cleaned_data['price']),
#                 'description': form.cleaned_data['description'],
#                 'rooms_available': str(form.cleaned_data['rooms_available']),
#                 'total_rooms': str(form.cleaned_data['total_rooms']),
#                 'country': form.cleaned_data['country'],
#                 'city': form.cleaned_data['city'],
#             }

#             # Handle file upload
#             files = None
#             if 'image' in request.FILES:
#                 files = {
#                     'image': (
#                         request.FILES['image'].name,
#                         request.FILES['image'],
#                         request.FILES['image'].content_type
#                     )
#                 }

#             # Get auth token from session
#             token = request.session.get('access_token')
#             if not token:
#                 messages.error(request, 'Please log in to continue.')
#                 return redirect('login')

#             headers = {'Authorization': f'Bearer {token}'}

#             if hotel_id:  # Edit existing hotel
#                 url = f'http://127.0.0.1:8000/api/edit-hotel/?hotel_id={hotel_id}'
#                 response = requests.put(
#                     url, data=data, files=files, headers=headers)
#             else:  # Create new hotel
#                 url = 'http://127.0.0.1:8000/api/create-hotel/'
#                 response = requests.post(
#                     url, data=data, files=files, headers=headers)

#             if response.status_code in [200, 201]:
#                 messages.success(request, 'Hotel saved successfully!')
#                 return redirect('hotel_list')
#             else:
#                 error_data = response.json()
#                 error_message = error_data.get('detail', 'An error occurred')
#                 messages.error(request, error_message)
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         # If editing, fetch hotel data
#         if hotel_id:
#             token = request.session.get('access_token')
#             if token:
#                 response = requests.get(
#                     f'http://127.0.0.1:8000/api/get-hotel/?hotel_id={hotel_id}',
#                     headers={'Authorization': f'Bearer {token}'}
#                 )
#                 if response.status_code == 200:
#                     hotel_data = response.json()
#                     form = HotelForm(initial=hotel_data)
#                 else:
#                     messages.error(request, 'Hotel not found')
#                     return redirect('hotel_list')
#         else:
#             form = HotelForm()

#     return render(request, 'hotels/hotel_form.html', {
#         'form': form,
#         'hotel_id': hotel_id,
#         'is_edit': bool(hotel_id)
#     })

from django.shortcuts import render
from django.contrib import messages
import requests
from django.http import JsonResponse
from Models.models import Hotel

# http://127.0.0.1:8000/Api_forms/hotel/edit/


def hotel_management(request, hotel_id=None):
    form = HotelForm()

    return render(request, 'Api_forms/hotel_form.html', {
                  'form': form, 'hotel_id': hotel_id})
