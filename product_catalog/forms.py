from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'car_name', 'brand', 'year', 'mileage', 'location', 'transmission', 'plate_type',
            'rear_camera', 'sun_roof', 'auto_retract_mirror', 'electric_parking_brake',
            'map_navigator', 'vehicle_stability_control', 'keyless_push_start', 'sports_mode',
            'camera_360_view', 'power_sliding_door', 'auto_cruise_control', 'price', 'instalment','image_url'
        ]
