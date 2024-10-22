from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserRole(models.TextChoices) :
    ADMIN = 'ADM', 'Admin',
    BUYER = 'BUY', 'Buyer',
    SELLER = 'SEL', 'Seller'

class UserRegion(models.TextChoices) :
    JAKARTA_UTARA = 'JAKUT', 'Jakarta Utara',
    JAKARTA_BARAT = 'JAKBAR', 'Jakarta Barat',
    JAKARTA_SELATAN = 'JAKSEL', 'Jakarta Selatan',
    JAKARTA_TIMUR = 'JAKTIM', 'Jakarta Timur',
    JAKARTA_PUSAT = 'JAKPUS', 'Jakarta Pusat'
    
class UserProfile(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    email = models.EmailField()
    role = models.CharField(default=UserRole.BUYER, choices=UserRole.choices, max_length=3)
    region = models.CharField(choices=UserRegion.choices, max_length=6)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)