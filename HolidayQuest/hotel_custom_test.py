import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HolidayQuest.settings')
django.setup()

from Models.models import Country, City, Hotel


def insert_and_test_hotel():
    # Step 1: Insert "Egypt" country if it doesn't exist
    country, created = Country.objects.get_or_create(name="Egypt")
    print(f"Country created: {created}, Country: {country.name}")

    # Step 2: Insert "Alex" city if it doesn't exist
    city, created = City.objects.get_or_create(
        name="sharm el sheikh", country=country)
    print(
        f"City created: {created}, City: {city.name}, Country: {city.country.name}")

    # Step 3: Insert "Morgana" hotel with the correct relationships
    hotel, created = Hotel.objects.get_or_create(
        name="Aida Hotel Sharm El Sheikh",
        city=city,
        country=country,
        address="123 Sharm El Sheikh St.",
        price=1500.00,
        description="A luxurious hotel in cairo.",
        rooms_available=10,
        total_rooms=50
    )
    print(
        f"Hotel created: {created}, Hotel: {hotel.name}, City: {hotel.city.name}, Country: {hotel.country.name}")

    # Step 4: Test relationships
    # Ensure the hotel is linked to the correct city and country
    assert hotel.city == city, f"Hotel's city should be {city.name}"
    assert hotel.country == country, f"Hotel's country should be {country.name}"

    # Step 5: Print out the details to verify
    print(
        f"Hotel {hotel.name} is located in {hotel.city.name}, {hotel.country.name}.")
    print(
        f"Hotel details: {hotel.address}, Price: {hotel.price}, Rooms available: {hotel.rooms_available}/{hotel.total_rooms}")

    # Optional: Confirm that the related hotel count in city and country is
    # correct
    print(f"Number of hotels in {city.name}: {city.hotels.count()}")
    print(f"Number of hotels in {country.name}: {country.hotels.count()}")


# Run the script
if __name__ == "__main__":
    insert_and_test_hotel()
