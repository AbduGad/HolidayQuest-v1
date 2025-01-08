import requests
from django.shortcuts import render
from .forms import HotelForm

# http://127.0.0.1:8000/create-hotel-form/


def create_hotel_form(request):
    print(request)
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        print(form.data)
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
        form = HotelForm()

    return render(request, 'HolidayQuest/create_hotel.html', {'form': form})
