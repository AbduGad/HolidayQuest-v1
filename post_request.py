import requests
import json

url = "http://127.0.0.1:8000/api/create-hotel/"
data = {
    "name": "Hotel D",
    "address": "123 d St.",
    "price": 199.99,
    "description": "A luxury hotel with beautiful views.",
    "rooms_available": 20,
    "total_rooms": 50,
    "country": "Egypt",  # country name
    "city": "Cairo"      # city name
}
response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
