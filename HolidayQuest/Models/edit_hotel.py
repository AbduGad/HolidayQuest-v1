import requests
hotel_id = 2
url = f"http://127.0.0.1:8000/api/edit-hotel/?hotel_id={hotel_id}"

data = {
    "price": 650

}


# Make the PUT request
response = requests.put(url, data=data)

# Check the response status and print the result
if response.status_code == 200:
    print("Hotel updated successfully:", response.json())
else:
    print("Failed to update hotel:", response.status_code, response.text)

# Close the file if opened
