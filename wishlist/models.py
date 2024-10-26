import uuid
from django.db import models
from django.contrib.auth.models import User
from product_catalog.models import Car


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'car']
        
    def __str__(self):
        return f"{self.car.car_name}"