import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bekas_berkelas.settings')
django.setup()

from django.contrib.auth.models import User
from authentication.models import UserProfile, UserRole 

names = [
    "Ramy", "Ultramy", "UltraRamy", "Naufal", "Muhammad",
    "Ramadhan", "Steven", "Setiawan", "Wida", "Putri",
    "Deanita", "Chip", "Skylar", "Case", "Shino",
    "Nadia", "Rahmadina", "Aristawati", "Okin", "Niko"
]
password = 'BekasBerkelas'

for name in names:
    username = name.lower()  
    email = f"{username}@gmail.com"

    user = User.objects.create_user(username=username, email=email, password=password)

    UserProfile.objects.create(
        user=user,
        name=name,
        email=email,
        no_telp='1234567890',
        role=UserRole.SELLER,  
        profile_picture=None,
        profile_picture_id=None,
        is_verified=True 
    )

print("Created user profiles with all verified and role as Seller.")
