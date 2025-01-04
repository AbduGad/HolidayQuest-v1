from django.test import TestCase
from .models import Country, City, Hotel
from django.utils import timezone


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
