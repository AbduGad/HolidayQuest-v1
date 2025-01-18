import requests
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2MzQzMzgzLCJpYXQiOjE3MzYyNTY5ODMsImp0aSI6Ijc0N2YwODRmY2NkMjQ2YzU5YTg2YWU4NzU3YjBiODZiIiwidXNlcl9pZCI6NH0.xlja7uTgWSYLGrtlfT0JPk3o2fTlxCqkOGcoNoV984E"

access_token2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2NDk3Nzc1LCJpYXQiOjE3MzY0MTEzNzUsImp0aSI6Ijg2ZmJkZmIyYWEwNzQ3MGNhZTQwODZmMDhmZjdjMzU0IiwidXNlcl9pZCI6NX0.itDvy2-a8WFu_FYRXwhEJnOUhRfmuvDfFpaR8AAYgFU"
headers = {
    "Authorization": f"Bearer {access_token2}"
    # Indicating that the data is in JSON format
}
url = "http://127.0.0.1:8000/user/user_created_hotels/"
re = requests.get(url, headers=headers)
print(re.status_code, re.content)
