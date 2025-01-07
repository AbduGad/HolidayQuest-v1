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
params = {'name': "Grand Hotel"}
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2MjMxOTE4LCJpYXQiOjE3MzYyMzE2MTgsImp0aSI6ImVhN2JmMGM2ZTY2MjRhMDFhZWEyNWZlNzA2NWJhYTIyIiwidXNlcl9pZCI6M30.MYkafGhwXNkfJnBCseV3RL8qtZf00Asqp3xph64ss5k"
refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNjMxODAxOCwiaWF0IjoxNzM2MjMxNjE4LCJqdGkiOiIxNTlkNTdjNDY4MTI0YWJiOWNjYzg5YzQ1ZGU4Zjg5OCIsInVzZXJfaWQiOjN9.FC9joj06BabbcZ05-64BYUVNeJb2BoKW--jbx4t3vMc"
# Headers including the access token


def refresh_access_token():
    response = requests.post(refresh_url, json={"refresh": refresh_token})
    if response.status_code == 200:
        return response.json().get("access")
    else:
        print(
            f"Failed to refresh token: {response.status_code}, {response.text}")
        return None


headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",  # Optional if sending JSON payload
}

# Send the PUT request with headers
response = requests.put(url, params=params, headers=headers)

# Handle the response
if response.status_code == 204:
    print('Hotel modified successfully')
else:
    print(f'Error: {response.status_code}, {response.text}')
