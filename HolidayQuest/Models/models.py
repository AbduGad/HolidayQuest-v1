from django.db import models
from PIL import Image  # Importing PIL for image manipulation if needed

# Country model


class Country(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# City model


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='cities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Hotel model


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='hotels')
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='hotels')
    address = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    rooms_available = models.IntegerField()
    total_rooms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='hotel_images/', null=True, blank=False)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     # If an image is provided, resize it to a maximum of 1024x1024 pixels
    #     if self.image:
    #         img = Image.open(self.image)
    #         if img.height > 1024 or img.width > 1024:
    #             img.thumbnail((1024, 1024))
    #             img.save(self.image.path)  # Save the resized image
    #     super().save(*args, **kwargs)
