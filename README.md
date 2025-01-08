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
- **AllowAny**: This API require authenticated users.
  if you are not you will get this error message
  ```json
  Authentication credentials were not provided.
  ```

## Serializer
- **HotelSerializer**: The hotel data is serialized using the `HotelSerializer` class, ensuring that the correct format is used for each hotel in the response.

## Error Handling
If there is an error with the request or pagination, the API will return a 400 status code with an error message explaining the issue.


---

# 3- Get Hotel Details API

## Endpoint
```
GET http://127.0.0.1:8000/api/get-hotel/
```

## Description
This API retrieves detailed information about a specific hotel by its `id` or `name`. If the hotel exists, its details are returned.

## Request Parameters

### Query Parameters
- **id** (integer, optional): The unique ID of the hotel to retrieve.
- **name** (string, optional): The name of the hotel to retrieve.

> **Note**: At least one of `id` or `hotel_name` is required.

### Example Request
#### By Hotel ID:
```plaintext
GET http://127.0.0.1:8000/api/get-hotel/?id=1
```

#### By Hotel Name:
```plaintext
GET http://127.0.0.1:8000/api/get-hotel/?hotel_name=Hotel%20D
```

## Response

### Success (HTTP 200 OK)
If the hotel is found, the API returns the hotel details in JSON format.

#### Example Response:
```json
{
  "id": 1,
  "name": "Hotel D",
  "address": "123 D St.",
  "price": 199.99,
  "description": "A luxury hotel with beautiful views.",
  "rooms_available": 20,
  "total_rooms": 50,
  "country": "Egypt",
  "city": "Cairo",
  "image": "http://127.0.0.1:8000/media/hotels/hotel_d.jpg"
}
```

### Error Responses

#### Missing Hotel Identifier (HTTP 400 Bad Request)
If neither `id` nor `name` is provided, the API will return an error.
```json
{
  "error": "Please provide either hotel id or name"
}
```

#### Hotel Not Found (HTTP 404 Not Found)
If no hotel is found matching the provided `id` or `name`, the API will return an error.
```json
{
  "error": "Hotel not found"
}
```

## Permissions
- **AllowAny**: This API does not restrict access, meaning any user can retrieve hotel details.

## Notes
- Ensure the hotel name provided is case-insensitive and matches exactly (use the `name` field stored in the database).
- This endpoint is useful for fetching individual hotel data when the user has specific identifiers.

---

# 4- Get Hotels by City , country or price range API

## Endpoint
```
GET http://127.0.0.1:8000/api/hotels/search?country=Jordan
```

## Description
This API retrieves a list of hotels based on location or price range filters. Users can search by country, city, minimum price, maximum price, or any combination of these criteria. If no filters are provided, the API will return an error.

## Request Parameters

### Query Parameters
- **country** (string, optional): The country where the hotel is located. *(Case-insensitive)*
- **city** (string, optional): The city where the hotel is located. *(Case-insensitive)*
- **min_price** (float, optional): The minimum price for a hotel.
- **max_price** (float, optional): The maximum price for a hotel.

### Example Request
```plaintext
GET http://127.0.0.1:8000/api/hotels/search?country=Egypt&city=luxor&min_price=50&max_price=600
```

## Response

### Success (HTTP 200 OK)
The request was successful, and the response will contain the list of hotels that match the provided filters.

#### Example Response:
```json
[
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
    "price": 250.00,
    "description": "A modern hotel with great amenities.",
    "rooms_available": 30,
    "total_rooms": 100,
    "country": "Egypt",
    "city": "Cairo",
    "image": "http://127.0.0.1:8000/media/hotels/hotel_e_image.jpg"
  }
]
```

### Error Responses

#### No Filters Provided (HTTP 400 Bad Request)
If no search criteria are provided, the API will return an error.
```json
{
  "error": "Please provide at least one search criteria (country, city, or price range)."
}
```

#### Invalid Price Value (HTTP 400 Bad Request)
If the `min_price` or `max_price` is not a valid number, the API will return an error.
```json
{
  "error": "Invalid minimum price value."
}
```

#### No Hotels Found (HTTP 404 Not Found)
If no hotels match the provided criteria, the API will return an error.
```json
{
  "error": "No hotels found for the given criteria."
}
```

#### Server Error (HTTP 500 Internal Server Error)
If there is an unexpected error, the API will return a generic error message.
```json
{
  "error": "An error occurred while processing your request."
}
```

## Filtering Logic
1. **Country**: Filters hotels by the exact name of the country (case-insensitive).
2. **City**: Filters hotels by the exact name of the city (case-insensitive).
3. **Price Range**:
   - `min_price`: Filters hotels with prices greater than or equal to the provided value.
   - `max_price`: Filters hotels with prices less than or equal to the provided value.
4. Results are combined to return only hotels that meet all provided filters.

## Permissions
- **AllowAny**: This API is accessible to all users, including unauthenticated users.

## Serializer
- **HotelSerializer**: The hotel data is serialized using the `HotelSerializer` class, ensuring a consistent format in the response.



---

# 5- Edit Hotel API

## Endpoint
```
PUT http://127.0.0.1:8000/api/edit-hotel/
```

## Description
This API allows users to update details of an existing hotel. The hotel can be identified either by its `hotel_id` or `hotel_name`. Only the fields provided in the request will be updated; other fields will remain unchanged.

## Request Parameters

### Query Parameters
- **hotel_id** (integer, optional): The unique ID of the hotel to be updated.
- **hotel_name** (string, optional): The name of the hotel to be updated.

> **Note**: At least one of `hotel_id` or `hotel_name` is required.

### Body Parameters
All fields are optional and will partially update the hotel record:
- **name** (string, optional): Updated name of the hotel.
- **address** (string, optional): Updated address of the hotel.
- **price** (float, optional): Updated price per night for the hotel.
- **description** (string, optional): Updated description of the hotel.
- **rooms_available** (integer, optional): Updated number of available rooms.
- **total_rooms** (integer, optional): Updated total number of rooms in the hotel.
- **country** (string, optional): Updated country name.
- **city** (string, optional): Updated city name.
- **image** (file, optional): Updated image of the hotel.

### Example Request
#### By Hotel ID:
```plaintext
PUT http://127.0.0.1:8000/api/edit-hotel/?hotel_id=1
```

#### By Hotel Name:
```plaintext
PUT http://127.0.0.1:8000/api/edit-hotel/?name=four%20seasons
```

#### Request Body (JSON):
```json
{
  "name": "Updated Hotel Name",
  "address": "Updated Address",
  "price": 299.99,
  "rooms_available": 15
}
```

#### Request Body (Multipart/Form-Data for Image Update):
```plaintext
{
  "image": <uploaded_image_file>
}
```

## Response

### Success (HTTP 200 OK)
The request was successful, and the updated hotel details are returned.

#### Example Response:
```json
{
  "id": 1,
  "name": "Updated Hotel Name",
  "address": "Updated Address",
  "price": 299.99,
  "description": "A newly updated description.",
  "rooms_available": 15,
  "total_rooms": 50,
  "country": "Egypt",
  "city": "Cairo",
  "image": "http://127.0.0.1:8000/media/hotels/updated_image.jpg"
}
```

### Error Responses

#### Missing Hotel Identifier (HTTP 400 Bad Request)
If neither `hotel_id` nor `hotel_name` is provided, the API will return an error.
```json
{
  "detail": "Hotel ID or name is required."
}
```

#### Hotel Not Found (HTTP 404 Not Found)
If no hotel is found matching the provided `hotel_id` or `hotel_name`, the API will return an error.
```json
{
  "detail": "Hotel not found."
}
```

#### Validation Errors (HTTP 400 Bad Request)
If any validation error occurs (e.g., invalid data types, invalid field values), the API will return the errors.
```json
{
  "price": ["Ensure this value is less than or equal to 10000."]
}
```

## Permissions
- You must be authorized to modify hotel details.  
  If not, you will receive the following error:  
  ```json
  status code 401 {"detail": "Authentication credentials were not provided."}
  ```

- Additionally, you must be the creator of the hotel to modify its details.  
  Otherwise, you will receive this error message:  
  ```json
  status code 403 {"detail": "You are not authorized to modify this hotel."}
  ```


## Notes
- If the `image` field is included, it must be sent as a file in a multipart/form-data request.
- Only the fields provided in the body will be updated. Unprovided fields will retain their existing values.

---

# 6- Delete Hotel API

## Endpoint
```
DELETE http://127.0.0.1:8000/api/delete-hotel/
```

## Description
This API allows users to delete a hotel by specifying either its `hotel_id` or `hotel_name`. If the hotel is found, it is removed from the database.

## Request Parameters

### Query Parameters
- **id** (integer, optional): The unique ID of the hotel to delete.
- **name** (string, optional): The name of the hotel to delete.

> **Note**: At least one of `hotel_id` or `hotel_name` is required.

### Example Request
#### By Hotel ID:
```plaintext
DELETE http://127.0.0.1:8000/api/delete-hotel/?id=1
```

#### By Hotel Name:
```plaintext
DELETE http://127.0.0.1:8000/api/delete-hotel/?name=four%20seasons
```

## Response

### Success (HTTP 204 No Content)
The hotel was successfully deleted from the database. No response body is returned.

#### Example Response:
```json
{
  "message": "Hotel deleted successfully"
}
```

### Error Responses

#### Missing Hotel Identifier (HTTP 400 Bad Request)
If neither `hotel_id` nor `hotel_name` is provided, the API will return an error.
```json
{
  "error": "Hotel ID or name is required"
}
```

#### Hotel Not Found (HTTP 404 Not Found)
If no hotel is found matching the provided `id` or `name`, the API will return an error.
```json
{
  "error": "Hotel not found"
}
```

## Permissions
- You must be authorized to delete a hotel.  
  If not, you will receive the following error:  
  ```json
  status code 401 {"detail": "Authentication credentials were not provided."}
  ```

- Additionally, you must be the creator of the hotel to delete it.  
  Otherwise, you will receive this error message:  
  ```json
  status code 403 {"detail": "You are not authorized to Delete this hotel."}
  ```
---

