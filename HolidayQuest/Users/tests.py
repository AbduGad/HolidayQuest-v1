from django.test import TestCase

# Create your tests here.
# import os
# import django

# # Set up Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HolidayQuest.settings')
# django.setup()

from Users.models import User

# Create a user using the custom manager
user = User.objects.create_user(
    email="john.doe@example.com",
    password="securepassword123",
    first_name="John",
    last_name="Doe"
)
print(user)
