import requests
import json

# url = "http://127.0.0.1:8000/api/create-hotel/"
# data = {
#     "name": "Hotel D",
#     "address": "123 d St.",
#     "price": 199.99,
#     "description": "A luxury hotel with beautiful views.",
#     "rooms_available": 20,
#     "total_rooms": 50,
#     "country": "Egypt",  # country name
#     "city": "Cairo"    # city name

# }
# files = {
#     "image": open("/mnt/c/Users/ahmed/Downloads/grand_hotel.jpeg", "rb"),
# }

# response = requests.post(url, data=data, files=files)
# print(response.status_code)
# print(response.json())
url = 'http://127.0.0.1:8000/api/edit-hotel/?hotel_id=1'

# Set the query parameter (hotel ID)
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2MjQ0NjYyLCJpYXQiOjE3MzYyNDQzNjIsImp0aSI6IjMzYTFmNzgxYWNmNzRjZWY5MDFhNTE5MzQxMTg5ZGQyIiwidXNlcl9pZCI6M30.-P9Nb0dMEofDtTIcv07NYH8mkBrda8p_Iyn3V98IvLI"
refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNjMyODc0MywiaWF0IjoxNzM2MjQyMzQzLCJqdGkiOiIxYzEwZTkxYmQ0ODQ0YmQ5YjhjZWNmNmE1NTU2M2VkMSIsInVzZXJfaWQiOjN9.38N3ewCdz7mRAP21zbgJq7hSIziDS_JFo70ae0s5oxQ"
# Headers including the access token
data = {
    'name': "small hotel"
}

# Access token

# Headers with Authorization and Content-Type
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",  # Indicating that the data is in JSON format
}

# Send the PUT request with the body as JSON
# Use json parameter instead of params
response = requests.put(url, json=data, headers=headers)

# Handle the response
if response.status_code == 200:
    print('Hotel modified successfully')
else:
    print(f'Error: {response.status_code}, {response.content}')
