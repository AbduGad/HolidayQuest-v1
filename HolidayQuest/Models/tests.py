from django.test import TestCase
from .models import Country, City, Hotel
from .serializers import HotelSerializer
from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from django.urls import reverse


class CountryModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Egypt")

    def test_country_creation(self):
        self.assertEqual(self.country.name, "Egypt")
        self.assertIsInstance(self.country.created_at, timezone.datetime)
        self.assertIsInstance(self.country.updated_at, timezone.datetime)

    def test_country_str(self):
        self.assertEqual(str(self.country), "Egypt")


class CityModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Egypt")
        self.city = City.objects.create(name="Cairo", country=self.country)

    def test_city_creation(self):
        self.assertEqual(self.city.name, "Cairo")
        self.assertEqual(self.city.country, self.country)
        self.assertIsInstance(self.city.created_at, timezone.datetime)
        self.assertIsInstance(self.city.updated_at, timezone.datetime)

    def test_city_str(self):
        self.assertEqual(str(self.city), "Cairo")


class HotelModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Egypt")
        self.city = City.objects.create(name="Cairo", country=self.country)
        self.hotel = Hotel.objects.create(
            name="Hotel Cairo",
            city=self.city,
            country=self.country,
            address="123 Cairo St.",
            price=100.00,
            description="A great hotel in Cairo.",
            rooms_available=10,
            total_rooms=100
        )

    def test_hotel_creation(self):
        self.assertEqual(self.hotel.name, "Hotel Cairo")
        self.assertEqual(self.hotel.city, self.city)
        self.assertEqual(self.hotel.country, self.country)
        self.assertEqual(self.hotel.address, "123 Cairo St.")
        self.assertEqual(self.hotel.price, 100.00)
        self.assertEqual(self.hotel.description, "A great hotel in Cairo.")
        self.assertEqual(self.hotel.rooms_available, 10)
        self.assertEqual(self.hotel.total_rooms, 100)
        self.assertIsInstance(self.hotel.created_at, timezone.datetime)
        self.assertIsInstance(self.hotel.updated_at, timezone.datetime)

    def test_hotel_str(self):
        self.assertEqual(str(self.hotel), "Hotel Cairo")


class HotelApiTest(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(name='Egypt')
        self.city = City.objects.create(name='Cairo', country=self.country)

        self.valid_data = {
            'name': 'Hotel A',
            'address': '123 Street, Cairo',
            'country': self.country.name,
            'city': self.city.name,
            "rooms_available": 10,
            "total_rooms": 50, "price": 250, "description": "some text"
        }
        with open("./media/hotel_images/4seasonjpg.jpg", "rb") as image_file:
            image_content = image_file.read()

        image = SimpleUploadedFile(
            name="4seasonjpg.jpg",
            content=image_content,
            content_type="image/jpeg"
        )
        self.valid_data["image"] = image

    def test_create_hotel(self):

        response = self.client.post(
            '/api/create-hotel/',
            data=self.valid_data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_hotel_with_missing_name(self):
        data_without_name = self.valid_data.copy()
        data_without_name['name'] = ""

        response = self.client.post(
            '/api/create-hotel/', data_without_name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the error is for the missing name field
        self.assertIn('name', response.data)

    def test_create_hotel_with_missing_country(self):
        data_without_name = self.valid_data.copy()
        data_without_name['country'] = ''

        response = self.client.post(
            '/api/create-hotel/',
            data=data_without_name,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the error is for the missing name field
        self.assertIn('country', response.data)

    def test_create_duplicate_hotel_with_same_name_different_address(self):
        import copy

        # Create complete data dictionary including the file
        complete_data = copy.deepcopy(self.valid_data)

        # Create the data for the second request
        data_with_diff_address = copy.deepcopy(complete_data)
        data_with_diff_address['address'] = "New address"
        # Need to create a new file object for the second request

        # First request
        first_response = self.client.post(
            '/api/create-hotel/',
            data=complete_data,
            format='multipart'
        )

        # Second request
        second_response = self.client.post(
            '/api/create-hotel/',
            data=data_with_diff_address,
            format='multipart'
        )

        error_detail = second_response.data['non_field_errors'][0]
        error_message = str(error_detail)

        self.assertEqual(
            error_message,
            'A hotel with the same name already exists'
        )

    def test_create_duplicate_hotel_with_same_address(self):
        import copy
        from django.core.files.uploadedfile import SimpleUploadedFile

        # Create a test image file

        # Create complete data dictionary including the file for first request
        complete_data = copy.deepcopy(self.valid_data)
        # Create data for second request with different name
        data_with_diff_name = copy.deepcopy(complete_data)
        data_with_diff_name['name'] = "new hotel !"
        # Need to create a new file object for the second request

        # First hotel creation
        first_res = self.client.post(
            '/api/create-hotel/',
            data=complete_data,
            format='multipart'
        )

        # Try to create the same hotel again with different name
        response = self.client.post(
            '/api/create-hotel/',
            data=data_with_diff_name,
            format='multipart'
        )

        error_detail = response.data['non_field_errors'][0]
        error_message = str(error_detail)

        self.assertEqual(
            error_message,
            'A hotel with the same address already exists'
        )


class EditHotelEndpointTests(APITestCase):
    def setUp(self):
        # Create a sample hotel for testing
        self.country = Country.objects.create(name='Egypt')
        self.city = City.objects.create(name='Cairo', country=self.country)

        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            address="123 Test St.",
            price=500,
            description="A test description.",
            rooms_available=10,
            total_rooms=20,
            country=self.country,
            city=self.city
        )
        # Update with the correct name if needed
        self.edit_hotel_url = reverse('edit-hotel')

    def test_edit_hotel_successful(self):
        """Test successful update of multiple fields of a hotel."""
        data = {
            "name": "Updated Hotel",
            "address": "456 New Address",
            "price": 650,
            "description": "Updated description.",
            "rooms_available": 15,
            "country": "Newland",
            "city": "New City"
        }
        response = self.client.put(
            f"{self.edit_hotel_url}?hotel_id={self.hotel.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the hotel's fields were updated
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.name, "Updated Hotel")
        self.assertEqual(self.hotel.address, "456 New Address")
        self.assertEqual(self.hotel.price, 650)
        self.assertEqual(self.hotel.description, "Updated description.")
        self.assertEqual(self.hotel.rooms_available, 15)
        self.assertEqual(self.hotel.country.name, "Newland")
        self.assertEqual(self.hotel.city.name, "New City")

    def test_edit_hotel_partial_update(self):
        """Test partial update of a hotel's fields."""
        data = {
            "price": 700,
            "rooms_available": 5
        }
        response = self.client.put(
            f"{self.edit_hotel_url}?hotel_id={self.hotel.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that only the specified fields were updated
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.price, 700)
        self.assertEqual(self.hotel.rooms_available, 5)
        self.assertEqual(self.hotel.name, "Test Hotel")  # Unchanged fields

    def test_edit_hotel_with_file(self):
        """Test updating a hotel with an image file."""
        with open("./media/hotel_images/4seasonjpg.jpg", "rb") as image:
            data = {
                "name": "Hotel With Image",
                "description": "Includes an image."
            }
            files = {"image": image}
            response = self.client.put(
                f"{self.edit_hotel_url}?hotel_id={self.hotel.id}",
                data,
                format='multipart',
                files=files)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Verify that the hotel's fields were updated
            self.hotel.refresh_from_db()
            self.assertEqual(self.hotel.name, "Hotel With Image")
            self.assertEqual(self.hotel.description, "Includes an image.")

    def tearDown(self):
        self.hotel.delete()

    def test_edit_hotel_partial_update_with_name(self):
        from urllib.parse import urlencode
        """Test partial update of a hotel's fields."""
        data = {
            "price": 700,
            "rooms_available": 5
        }
        params = {'hotel_name': 'Test Hotel'}
        url_with_query = f"{self.edit_hotel_url}?{urlencode(params)}"

        response = self.client.put(url_with_query, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that only the specified fields were updated
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.price, 700)
        self.assertEqual(self.hotel.rooms_available, 5)
        self.assertEqual(self.hotel.name, "Test Hotel")  # Unchanged fields
