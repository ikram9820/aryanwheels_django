from uuid import uuid4
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import validate_file_size


class Seller(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='seller')
    whatsapp_contact = models.BigIntegerField(blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True, null=True)
    bio= models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name', 'user__date_joined']

class Follow(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='follower')
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE,related_name='following')

class Vehicles(models.Model):
    VEHICLES_TYPE_TRUCK = 'T'
    VEHICLES_TYPE_CAR = 'C'
    VEHICLES_TYPE_BIKE = 'B'
    VEHICLES_TYPE_PART = 'P'

    VEHICLES_TYPE_CHOICES = [
        (VEHICLES_TYPE_TRUCK, 'Truck'),
        (VEHICLES_TYPE_CAR, 'Car'),
        (VEHICLES_TYPE_BIKE, 'Bike'),
        (VEHICLES_TYPE_PART, 'Part'),
    ]

    owner = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name='vehicles')
    vehicles_type = models.CharField(
        max_length=1, choices=VEHICLES_TYPE_CHOICES, default=VEHICLES_TYPE_CAR)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    slug = models.SlugField()
    model_year = models.IntegerField(
        validators=[MinValueValidator(1970), MaxValueValidator(2023)])
    distance_traveled = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    price = models.DecimalField(
        max_digits=9, decimal_places=0, validators=[MinValueValidator(0)])
    posting_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.manufacturer} {self.model} {self.model_year}'

    class Meta:
        ordering = ['posting_date']


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        Vehicles, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='showroom/images',
                              validators=[validate_file_size])




class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='like', null=True)
    liked_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f'like started by {self.user} at {self.liked_at}'


class LikedItem(models.Model):
    like = models.ForeignKey(
        Like, on_delete=models.CASCADE, related_name='liked_item')
    vehicle = models.ForeignKey(
        Vehicles, on_delete=models.CASCADE, related_name='liked_vehicle')

    def __str__(self) -> str:
        return f'{self.vehicle} added to {self.like}'

    class Meta:
        unique_together = [['like', 'vehicle']]
