import requests
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2MzQzMzgzLCJpYXQiOjE3MzYyNTY5ODMsImp0aSI6Ijc0N2YwODRmY2NkMjQ2YzU5YTg2YWU4NzU3YjBiODZiIiwidXNlcl9pZCI6NH0.xlja7uTgWSYLGrtlfT0JPk3o2fTlxCqkOGcoNoV984E"

access_token2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2Mzg0OTI1LCJpYXQiOjE3MzYyOTg1MjUsImp0aSI6IjFjY2IzMmJjM2FiZDQxMDJiNGQ5YWM5NWNmNTk0OTFhIiwidXNlcl9pZCI6NX0.Tku-LFS7KU1bmBeN2TCkbBQkW0XUTtxLycKqK4PuCYo"
headers = {
    "Authorization": f"Bearer {access_token2}"
    # Indicating that the data is in JSON format
}
url = "http://127.0.0.1:8000/api/edit-hotel/?hotel_name=Alex%20New%20Hotel"
data = {"name": "New Hotel", "price": 1000}
re = requests.put(url, data=data, headers=headers)
print(re.status_code, re.content)
