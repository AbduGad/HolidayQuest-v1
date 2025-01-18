import requests
import json
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2MzQzMzgzLCJpYXQiOjE3MzYyNTY5ODMsImp0aSI6Ijc0N2YwODRmY2NkMjQ2YzU5YTg2YWU4NzU3YjBiODZiIiwidXNlcl9pZCI6NH0.xlja7uTgWSYLGrtlfT0JPk3o2fTlxCqkOGcoNoV984E"

access_token2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2Mzg0OTI1LCJpYXQiOjE3MzYyOTg1MjUsImp0aSI6IjFjY2IzMmJjM2FiZDQxMDJiNGQ5YWM5NWNmNTk0OTFhIiwidXNlcl9pZCI6NX0.Tku-LFS7KU1bmBeN2TCkbBQkW0XUTtxLycKqK4PuCYo"
headers = {
    "Authorization": f"Bearer {access_token2}"
    # Indicating that the data is in JSON format
}

post_url = "http://127.0.0.1:8000/api/create-hotel/"
data = {
    "name": "New Hotel",
    "address": "Alex , egy",
    "price": 199.99,
    "description": "A luxury hotel with beautiful views in Alex.",
    "rooms_available": 30,
    "total_rooms": 800,
    "country": "Egypt",  # country name
    "city": "Alex",
    "created_by": {"id": 1, "first_name": "ahmed", "last_name": "amr", "email": "dev.ahmedamr989@gmail.com"}
}


def post():
    delete_url = 'http://127.0.0.1:8000/api/delete-hotel/?hotel_name=New%20Hotel'

    response = requests.delete(delete_url, headers=headers)

    if response.status_code == 204:
        print("deletion was successful!")
        print(response.text)  # Print the response content
    else:
        print(
            f"Request failed with status code {response.status_code}",
            response.content)

    files = {
        "image": open("/mnt/c/Users/ahmed/Downloads/grand_hotel.jpeg", "rb"),
    }

    response = requests.post(post_url, data=data, files=files, headers=headers)
    print(response.status_code)
    print(response.content)
    # url = 'http://127.0.0.1:8000/api/delete-hotel/?hotel_name=New%20Hotel'
    # Set the query parameter (hotel ID)
    refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2MjU1NDcxLCJpYXQiOjE3MzYyNTUxNzEsImp0aSI6ImY1OTI3YWE0NTNlNDQ5Y2E4Y2UyNDQ1ODEwMTdjYmIxIiwidXNlcl9pZCI6NH0.J2Vs2O4WhT7dW4Kzf-dJLL6c4HkAoUa6VDeDBemo2VA"


post()
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
