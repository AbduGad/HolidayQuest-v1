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
url = 'http://127.0.0.1:8000/api/delete-hotel/'

# Set the query parameter (hotel ID)
params = {'name': "menoufia Hotel"}

# Send the DELETE request
response = requests.delete(url, params=params)

# Print the response from the server
if response.status_code == 204:
    print('Hotel deleted successfully')
else:
    print(f'Error: {response.status_code}', response.content)
