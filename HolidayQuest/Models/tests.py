from django.test import TestCase
from .models import Country, City, Hotel
from .serializers import HotelSerializer
from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status


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

    def test_create_hotel(self):
        response = self.client.post(
            '/api/create-hotel/',
            self.valid_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_hotel_with_missing_name(self):
        data_without_name = self.valid_data.copy()
        data_without_name['name'] = None

        response = self.client.post(
            '/api/create-hotel/', data_without_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the error is for the missing name field
        self.assertIn('name', response.data)

    def test_create_hotel_with_missing_country(self):
        data_without_name = self.valid_data.copy()
        data_without_name['country'] = ''

        response = self.client.post(
            '/api/create-hotel/',
            data_without_name,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the error is for the missing name field
        self.assertIn('country', response.data)

    def test_create_duplicate_hotel_with_same_name_different_address(self):
        import copy
        data_with_diff_Address = copy.deepcopy(self.valid_data)
        data_with_diff_Address["address"] = "New address"

        # Try to create the same hotel again
        first_response = self.client.post(
            '/api/create-hotel/',
            self.valid_data, format='json')

        second_response = self.client.post(
            '/api/create-hotel/',
            data_with_diff_Address, format='json')

        error_detail = second_response.data['non_field_errors'][0]
        # Convert ErrorDetail to its string representation
        error_message = str(error_detail)

        # Now assert against the expected error message string
        self.assertEqual(
            error_message,
            'A hotel with the same name already exists'
        )

    def test_create_duplicate_hotel_with_same_address(self):
        import copy
        data_with_diff_Name = copy.deepcopy(self.valid_data)
        data_with_diff_Name["name"] = "new hotel !"
        # First hotel creation
        self.client.post('/api/create-hotel/', self.valid_data, format='json')

        # Try to create the same hotel again
        response = self.client.post(
            '/api/create-hotel/', data_with_diff_Name, format='json')

        # This is an ErrorDetail object
        error_detail = response.data['non_field_errors'][0]
        # Convert ErrorDetail to its string representation
        error_message = str(error_detail)

        # Now assert against the expected error message string
        self.assertEqual(
            error_message,
            'A hotel with the same address already exists'
        )
