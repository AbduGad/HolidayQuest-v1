import requests
import json
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2MjU2Mjk1LCJpYXQiOjE3MzYyNTU5OTUsImp0aSI6IjZiZDlmNzZlYjM0NTQ0NTg5NjczYTYyMTViMWJhYTI3IiwidXNlcl9pZCI6NH0.-eo52wq1A-CIJq313xIzybTxG5Qmit5FlUa-c6Az2fs"
headers = {
    "Authorization": f"Bearer {access_token}"
    # Indicating that the data is in JSON format
}

url = "http://127.0.0.1:8000/api/create-hotel/"
data = {
    "name": "New Hotel",
    "address": "Alex , egy",
    "price": 199.99,
    "description": "A luxury hotel with beautiful views in Alex.",
    "rooms_available": 30,
    "total_rooms": 800,
    "country": "Egypt",  # country name
    "city": "Alex"    # city name

}
files = {
    "image": open("/mnt/c/Users/ahmed/Downloads/grand_hotel.jpeg", "rb"),
}

response = requests.post(url, data=data, files=files, headers=headers)
print(response.status_code)
print(response.content)
url = 'http://127.0.0.1:8000/api/edit-hotel/?hotel_id=1'

# Set the query parameter (hotel ID)
refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2MjU1NDcxLCJpYXQiOjE3MzYyNTUxNzEsImp0aSI6ImY1OTI3YWE0NTNlNDQ5Y2E4Y2UyNDQ1ODEwMTdjYmIxIiwidXNlcl9pZCI6NH0.J2Vs2O4WhT7dW4Kzf-dJLL6c4HkAoUa6VDeDBemo2VA"
# Headers including the access token
# data = {
#     'name': "small hotel"
# }

# # Access token

# # Headers with Authorization and Content-Type
# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json",  # Indicating that the data is in JSON format
# }

# # Send the PUT request with the body as JSON
# # Use json parameter instead of params
# response = requests.put(url, json=data, headers=headers)

# # Handle the response
# if response.status_code == 200:
#     print('Hotel modified successfully')
# else:
#     print(f'Error: {response.status_code}, {response.content}')
