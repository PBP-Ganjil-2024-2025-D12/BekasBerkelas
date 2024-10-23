import os
import csv
import django

# Set the environment variable to your Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BebasBerkelas.settings')

# Initialize Django
django.setup()

from product_catalog.models import Car  # Import the Car model from your app

def import_cars(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Create a Car object for each row in the CSV
            car = Car(
                car_name=row['car_name'],
                brand=row['brand'],
                year=int(row['year']),
                mileage=int(row['mileage']),
                location=row['location'],
                transmission=row['transmission'],
                plate_type=row['plate type'],  # Adjusted to match your CSV header
                rear_camera=row['rear camera'] == '1',  # Adjusted for CSV input
                sun_roof=row['sun roof'] == '1',  # Adjusted for CSV input
                auto_retract_mirror=row['auto retract mirror'] == '1',  # Adjusted for CSV input
                electric_parking_brake=row.get('electric parking brake') == '1',  # Check for new fields
                map_navigator=row.get('map navigator') == '1',  # Check for new fields
                vehicle_stability_control=row.get('vehicle stability control') == '1',  # Check for new fields
                keyless_push_start=row.get('keyless push start') == '1',  # Check for new fields
                sports_mode=row.get('sports mode') == '1',  # Check for new fields
                camera_360_view=row.get('360 camera view') == '1',  # Check for new fields
                power_sliding_door=row.get('power sliding door') == '1',  # Check for new fields
                auto_cruise_control=row.get('auto cruise control') == '1',  # Check for new fields
                price=float(row['price (Rp)']),  # Adjusted for price
                instalment=float(row['instalment (Rp|Monthly)']),  # Adjusted for instalment
            )
            car.save()  # Save the car object to the database
            print(f'Successfully added car: {car.car_name}')

if __name__ == "__main__":
    # Replace 'path/to/your/filtered_car_data.csv' with the actual path to your CSV file
    import_cars('filtered_car_data.csv')
