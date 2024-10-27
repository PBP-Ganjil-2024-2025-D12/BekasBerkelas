import os
import django

# Set the settings module (replace 'yourproject.settings' with your actual settings module)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bekas_berkelas.settings')
django.setup()

from django.contrib.auth.models import User
from authentication.models import UserProfile, UserRole  # Replace 'yourapp' with your app's name

names = [
    "Ramy", "Ultramy", "UltraRamy", "Naufal", "Muhammad",
    "Ramadhan", "Steven", "Setiawan", "Wida", "Putri",
    "Deanita", "Chip", "Skylar", "Case", "Shino",
    "Nadia", "Rahmadina", "Aristawati", "Okin", "Niko"
]
password = 'BekasBerkelas'

for name in names:
    username = name.lower()  # Convert to lowercase for username
    email = f"{username}@gmail.com"

    # Create User
    user = User.objects.create_user(username=username, email=email, password=password)

    # Create UserProfile with is_verified=True and role=SELLER
    UserProfile.objects.create(
        user=user,
        name=name,
        email=email,
        no_telp='1234567890',
        role=UserRole.SELLER,  # Set role as SELLER
        profile_picture=None,
        profile_picture_id=None,
        is_verified=True  # Set verified to True
    )

print("Created user profiles with all verified and role as Seller.")
