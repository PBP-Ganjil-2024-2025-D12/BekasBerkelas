from django.db import models

class Car(models.Model):
    CAR_TRANSMISSION_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]
    
    PLATE_TYPE_CHOICES = [
        ('Even', 'Even'),
        ('Odd', 'Odd'),
    ]
    
    car_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    transmission = models.CharField(max_length=10, choices=CAR_TRANSMISSION_CHOICES)
    plate_type = models.CharField(max_length=10, choices=PLATE_TYPE_CHOICES)
    rear_camera = models.BooleanField(default=False)
    sun_roof = models.BooleanField(default=False)
    auto_retract_mirror = models.BooleanField(default=False)

