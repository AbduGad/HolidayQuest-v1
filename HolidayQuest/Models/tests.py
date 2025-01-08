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
from Users.models import User
from rest_framework.authtoken.models import Token


class CountryModelTest(
        # TestCase
):
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
        self.user = User.objects.create_user(email="testuser@g.com",
                                             first_name='testuser', last_name="user", password='testpassword')
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
            total_rooms=100,
            created_by=self.user
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
        self.user = User.objects.create_user(email="testuser@g.com",
                                             first_name='testuser', last_name="user", password='testpassword')

        # Obtain the access token for the user
        login_data = {
            'email': 'testuser@g.com',
            'password': 'testpassword'
        }
        login_response = self.client.post(
            '/user/login/', data=login_data)  # Adjust URL if necessary
        # Assuming the response contains the 'access' token
        self.user_token = login_response.data['access']

        # Add the Authorization header with the AccessToken
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)

        self.valid_data = {
            'name': 'Hotel A',
            'address': '123 Street, Cairo',
            'country': self.country.name,
            'city': self.city.name,
            "rooms_available": 10,
            "total_rooms": 50, "price": 250, "description": "some text",
            "created_by": self.user, "user_id": self.user.id
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


class EditHotelEndpointTests(
    APITestCase
):
    def setUp(self):
        # Create a sample hotel for testing
        self.user = User.objects.create_user(email="testuser@g.com",
                                             first_name='testuser', last_name="user", password='testpassword')
        self.country = Country.objects.create(name='Egypt')
        self.city = City.objects.create(
            name='Cairo', country=self.country)
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            address="123 Test St.",
            price=500,
            description="A test description.",
            rooms_available=10,
            total_rooms=20,
            country=self.country,
            city=self.city,
            created_by=self.user,
        )
        login_data = {
            'email': 'testuser@g.com',
            'password': 'testpassword'
        }
        login_response = self.client.post('/user/login/', data=login_data)
        if login_response.status_code == 200:
            # Get the access token
            self.user_token = login_response.data['access']
        else:
            self.fail('Failed to retrieve access token')

        # Add the Authorization header with the AccessToken
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)

        # Set the URL for editing the hotel (ensure this URL is correct in your
        # project)
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


from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Hotel, Country, City
from decimal import Decimal
import os


class HotelViewTests(
    APITestCase
):

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@g.com",
                                             first_name='testuser', last_name="user", password='testpassword')
        # Create test image
        self.image_path = os.path.join(
            os.path.dirname(__file__),
            'hotel_images',
            'test_hotel.jpg')
        self.test_image = SimpleUploadedFile(
            name='test_hotel.jpg',
            content=open(self.image_path, 'rb').read(),
            content_type='image/jpeg'
        )

        # Create countries
        self.country1 = Country.objects.create(name="Egypt")
        self.country2 = Country.objects.create(name="UAE")

        # Create cities
        self.city1 = City.objects.create(name="Cairo", country=self.country1)
        self.city2 = City.objects.create(
            name="Alexandria", country=self.country1)
        self.city3 = City.objects.create(name="Dubai", country=self.country2)

        self.hotel1 = Hotel.objects.create(
            name="Hotel A",
            address="123 A St.",
            price=Decimal('199.99'),
            description="A luxury hotel with beautiful views.",
            rooms_available=20,
            total_rooms=50,
            country=self.country1,
            city=self.city1,
            image=self.test_image,
            created_by=self.user
        )

        self.hotel2 = Hotel.objects.create(
            name="Hotel B",
            address="456 B St.",
            price=Decimal('149.99'),
            description="A comfortable mid-range hotel.",
            rooms_available=15,
            total_rooms=40,
            country=self.country1,
            city=self.city1,
            image=self.test_image,
            created_by=self.user
        )

        self.hotel3 = Hotel.objects.create(
            name="Hotel C",
            address="789 C St.",
            price=Decimal('299.99'),
            description="A luxury resort by the sea.",
            rooms_available=25,
            total_rooms=60,
            country=self.country1,
            city=self.city2,
            image=self.test_image,
            created_by=self.user
        )

        # Update the URL to match the actual API endpoint
        self.url = '/api/hotels/search'  # Direct URL instead of using reverse()

    def tearDown(self):
        # Clean up uploaded files after tests
        for hotel in Hotel.objects.all():
            if hotel.image:
                if os.path.exists(hotel.image.path):
                    os.remove(hotel.image.path)

    def test_no_parameters(self):
        """Test that request without any parameters returns 400"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_by_country(self):
        """Test filtering hotels by country"""
        response = self.client.get(self.url, {'country': 'Egypt'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # Verify image URL is present in response
        self.assertTrue('image' in response.data[0])

    def test_filter_by_city(self):
        """Test filtering hotels by city"""
        response = self.client.get(self.url, {'city': 'Cairo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Verify hotel details
        self.assertEqual(response.data[0]['rooms_available'], 20)
        self.assertEqual(response.data[0]['total_rooms'], 50)

    def test_filter_by_price_range(self):
        """Test filtering hotels by price range"""
        response = self.client.get(self.url, {
            'min_price': '150',
            'max_price': '250'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # Verify hotel details
        self.assertEqual(response.data[0]['name'], 'Hotel A')
        self.assertEqual(float(response.data[0]['price']), 199.99)

        def test_combined_filters(self):
            """Test filtering with multiple parameters"""
        response = self.client.get(self.url, {
            'country': 'Egypt',
            'city': 'Cairo',
            'min_price': '190',  # Changed from 100 to 190 to only catch Hotel A
            'max_price': '200'   # Kept at 200
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Now should only get Hotel A

        # Verify complete hotel details
        hotel = response.data[0]
        self.assertEqual(hotel['name'], 'Hotel A')
        self.assertEqual(hotel['address'], '123 A St.')
        self.assertEqual(float(hotel['price']), 199.99)
        self.assertEqual(
            hotel['description'],
            'A luxury hotel with beautiful views.')
        self.assertEqual(hotel['rooms_available'], 20)
        self.assertEqual(hotel['total_rooms'], 50)
        self.assertTrue('image' in hotel)

    def test_invalid_price_values(self):
        """Test handling of invalid price values"""
        response = self.client.get(self.url, {'min_price': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_results(self):
        """Test when no hotels match the criteria"""
        response = self.client.get(self.url, {
            'country': 'France'  # Country that doesn't exist in test data
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_case_insensitive_search(self):
        """Test that country and city searches are case insensitive"""
        response = self.client.get(self.url, {'country': 'egypt'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        response = self.client.get(self.url, {'city': 'CAIRO'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
