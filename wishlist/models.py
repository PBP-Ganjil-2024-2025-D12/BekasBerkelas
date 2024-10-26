from django.db import models
from django.contrib.auth.models import User
from product_catalog.models import Car

class Wishlist(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.car.name} (Priority: {self.get_priority_display()})"
