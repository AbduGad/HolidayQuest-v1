from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        '''
        Creates and saves a User with the given email and password.
        '''
        if not email:
            raise ValueError("The Email field must be set")
        # normalize_email() keeps the entered email in lower cases
        email = self.normalize_email(email)
        # self.model equates to User() class
        user = self.model(email=email, **extra_fields)
        # Hash the password
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        '''
        Creates and saves a superuser with the given email and password.
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Assign the custom UserManager
    objects = UserManager()

    '''
    The USERNAME_FIELD attribute specifies the field in your model that will be used
    as the unique identifier for the user. By default, Django uses the username
    '''
    USERNAME_FIELD = 'email'
    '''
    The REQUIRED_FIELDS attribute specifies a list of fields that must be provided when using
    the createsuperuser management command or when creating a user programmatically.
    These fields are in addition to the USERNAME_FIELD, which is always required.
    '''
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def clean(self):
        '''
        Cutom clean used by the EmailField() method to print custom error message.
        '''
        if '@' not in self.email:
            raise ValidationError({'email': 'The email must contain an "@" symbol.'})

    def __str__(self):
        '''
        Return a string representation of the user's email
        '''
        return self.email
