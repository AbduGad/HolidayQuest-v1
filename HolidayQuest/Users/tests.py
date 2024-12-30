from django.test import TestCase

# Create your tests here.

from django.core.exceptions import ValidationError
from Users.models import User

class UserModelTest(TestCase):
    
    def test_invalid_email(self):
        """Test that an invalid email raises a ValidationError"""
        with self.assertRaises(ValidationError):
            user = User.objects.create_user(
                email="invalid-email",  # Invalid email format
                password="securepassword123",
                first_name="John",
                last_name="Doe"
            )
            user.full_clean()  # This will run the validation

    def test_valid_email(self):
        """Test that a valid email works without errors"""
        user = User.objects.create_user(
            email="john.doe@example.com",  # Valid email format
            password="securepassword123",
            first_name="John",
            last_name="Doe"
        )
        user.full_clean()  # This will run the validation
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertTrue(user.check_password("securepassword123"))
    
    def test_email_contains_at_symbol(self):
        """Test that the email contains '@'"""
        user = User.objects.create_user(
            email="john.doe@example.com",  # Valid email format
            password="securepassword123",
            first_name="John",
            last_name="Doe"
        )
        # Check if email contains '@'
        self.assertIn('@', user.email)





# # import os
# # import django

# # # Set up Django environment
# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HolidayQuest.settings')
# # django.setup()

# from Users.models import User

# # Create a user using the custom manager
# user = User.objects.create_user(
#     email="john.doe@example.com",
#     password="securepassword123",
#     first_name="John",
#     last_name="Doe"
# )
# print(user)
# user.delete()

# from django.core.exceptions import ValidationError

# user = User(
#     email="john.doeexample.com",
#     password="securepassword123",
#     first_name="John",
#     last_name="Doe"
# )

# try:
#     user.full_clean()  # This will run model-level validations
#     user.save()
#     print(user)
# except ValidationError as e:
#     print("Validation Error:", e)
