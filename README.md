# 1- Create Hotel API

## Endpoint
```
POST http://127.0.0.1:8000/api/create-hotel/
```

## Description
This API allows the creation of a new hotel entry in the system. The request must include all required hotel data, including the hotel's name, address, price, description, available rooms, total rooms, country, city, and an image. All fields are required.

## Request Parameters

### Body (Form Data)
- **name** (string): The name of the hotel. *(Required)*
- **address** (string): The street address of the hotel. *(Required)*
- **price** (float): The price per night for staying at the hotel. *(Required)*
- **description** (string): A description of the hotel. *(Required)*
- **rooms_available** (integer): The number of rooms available in the hotel. *(Required)*
- **total_rooms** (integer): The total number of rooms in the hotel. *(Required)*
- **country** (string): The country where the hotel is located. *(Required)*
- **city** (string): The city where the hotel is located. *(Required)*
- **image** (file): An image of the hotel (e.g., a photo of the exterior or interior). *(Required)*

### Example Request Body
```plaintext
name=Hotel D
address=123 d St.
price=199.99
description=A luxury hotel with beautiful views.
rooms_available=20
total_rooms=50
country=Egypt
city=Cairo
image=[file]
```

## Response

### Success (HTTP 201 Created)
The request was successful, and the hotel data has been created. The response will include the hotel data.

#### Example Response:
```json
{
  "id": 1,
  "name": "Hotel D",
  "address": "123 d St.",
  "price": 199.99,
  "description": "A luxury hotel with beautiful views.",
  "rooms_available": 20,
  "total_rooms": 50,
  "country": "Egypt",
  "city": "Cairo",
  "image": "http://127.0.0.1:8000/media/hotels/hotel_d_image.jpg"
}
```

### Error (HTTP 400 Bad Request)
If the required fields are missing or invalid, the response will contain detailed error messages indicating what went wrong.

#### Example Response:
```json
{
  "name": ["This field is required."],
  "address": ["This field is required."],
  "price": ["This field is required."],
  "description": ["This field is required."],
  "rooms_available": ["This field is required."],
  "total_rooms": ["This field is required."],
  "country": ["This field is required."],
  "city": ["This field is required."],
  "image": ["This field is required."]
}
```

## Permissions
- **AllowAny**: This API is accessible to all users, including unauthenticated users.

## Serializer
- **HotelSerializer**: The data is validated using the `HotelSerializer` class, which ensures that all fields are correctly formatted and required fields are present.

## Error Handling
If any of the required fields are missing or invalid, the API will return a 400 status code with a detailed error message, specifying which fields are missing or incorrect.


---

# 2- Get Hotels API

## Endpoint
```
GET http://127.0.0.1:8000/api/get-hotels/
```

## Description
This API retrieves a list of hotels from the system. It supports pagination to limit the number of hotels returned per request. The request does not require any input parameters, and the response contains the list of hotels in a paginated format.

## Request Parameters

- **None**: This is a `GET` request, and no parameters are required in the request body.

## Response

### Success (HTTP 200 OK)
The request was successful, and the response will contain the list of hotels in a paginated format.

#### Example Response:
```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/get-hotels/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Hotel D",
      "address": "123 d St.",
      "price": 199.99,
      "description": "A luxury hotel with beautiful views.",
      "rooms_available": 20,
      "total_rooms": 50,
      "country": "Egypt",
      "city": "Cairo",
      "image": "http://127.0.0.1:8000/media/hotels/hotel_d_image.jpg"
    },
    {
      "id": 2,
      "name": "Hotel E",
      "address": "456 e Ave.",
      "price": 299.99,
      "description": "A modern hotel with great amenities.",
      "rooms_available": 30,
      "total_rooms": 100,
      "country": "Egypt",
      "city": "Alexandria",
      "image": "http://127.0.0.1:8000/media/hotels/hotel_e_image.jpg"
    }
  ]
}
```

### Error (HTTP 400 Bad Request)
If the request is malformed or any error occurs in fetching data, the response will contain an error message.

#### Example Response:
```json
{
  "detail": "Invalid parameters or pagination error."
}
```

## Pagination
The response is paginated. It will return the number of results available in the `count` field, and links to the next and previous pages are included in the `next` and `previous` fields. The `results` field will contain the current page's data.

- **count**: The total number of hotels available in the system.
- **next**: A URL to fetch the next page of results (if available).
- **previous**: A URL to fetch the previous page of results (if available).
- **results**: An array containing the hotels on the current page.

## Permissions
- **AllowAny**: This API is accessible to all users, including unauthenticated users.

## Serializer
- **HotelSerializer**: The hotel data is serialized using the `HotelSerializer` class, ensuring that the correct format is used for each hotel in the response.

## Error Handling
If there is an error with the request or pagination, the API will return a 400 status code with an error message explaining the issue.


