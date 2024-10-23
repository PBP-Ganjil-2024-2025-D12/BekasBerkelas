import uuid
from django.db import models
from django.contrib.auth.models import User
from product_catalog.models import Car


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.car.car_name}"