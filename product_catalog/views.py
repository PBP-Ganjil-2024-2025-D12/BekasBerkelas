from django.shortcuts import render, redirect
from .models import Car
from django.contrib.auth.decorators import login_required
from .forms import CarForm, CarFilterForm
from authentication.models import UserProfile  # Adjust the import according to your app structure
from django.shortcuts import get_object_or_404

@login_required
def car_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    cars = Car.objects.all()
    form = CarFilterForm(request.GET)

    if form.is_valid():
        car_name = form.cleaned_data.get('car_name')
        brand = form.cleaned_data.get('brand')
        year = form.cleaned_data.get('year')
        mileage = form.cleaned_data.get('mileage')
        location = form.cleaned_data.get('location')
        transmission = form.cleaned_data.get('transmission')
        plate_type = form.cleaned_data.get('plate_type')
        rear_camera = form.cleaned_data.get('rear_camera')
        sun_roof = form.cleaned_data.get('sun_roof')
        auto_retract_mirror = form.cleaned_data.get('auto_retract_mirror')
        electric_parking_brake = form.cleaned_data.get('electric_parking_brake')
        map_navigator = form.cleaned_data.get('map_navigator')
        vehicle_stability_control = form.cleaned_data.get('vehicle_stability_control')
        keyless_push_start = form.cleaned_data.get('keyless_push_start')
        sports_mode = form.cleaned_data.get('sports_mode')
        camera_360_view = form.cleaned_data.get('camera_360_view')
        power_sliding_door = form.cleaned_data.get('power_sliding_door')
        auto_cruise_control = form.cleaned_data.get('auto_cruise_control')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')
        instalment_min = form.cleaned_data.get('instalment_min')
        instalment_max = form.cleaned_data.get('instalment_max')

        if car_name:
            cars = cars.filter(car_name__icontains=car_name)
        if brand:
            cars = cars.filter(brand__icontains=brand)
        if year:
            cars = cars.filter(year=year)
        if mileage:
            cars = cars.filter(mileage=mileage)
        if location:
            cars = cars.filter(location__icontains=location)
        if transmission:
            cars = cars.filter(transmission=transmission)
        if plate_type:
            cars = cars.filter(plate_type=plate_type)
        if rear_camera is not None:
            cars = cars.filter(rear_camera=rear_camera)
        if sun_roof is not None:
            cars = cars.filter(sun_roof=sun_roof)
        if auto_retract_mirror is not None:
            cars = cars.filter(auto_retract_mirror=auto_retract_mirror)
        if electric_parking_brake is not None:
            cars = cars.filter(electric_parking_brake=electric_parking_brake)
        if map_navigator is not None:
            cars = cars.filter(map_navigator=map_navigator)
        if vehicle_stability_control is not None:
            cars = cars.filter(vehicle_stability_control=vehicle_stability_control)
        if keyless_push_start is not None:
            cars = cars.filter(keyless_push_start=keyless_push_start)
        if sports_mode is not None:
            cars = cars.filter(sports_mode=sports_mode)
        if camera_360_view is not None:
            cars = cars.filter(camera_360_view=camera_360_view)
        if power_sliding_door is not None:
            cars = cars.filter(power_sliding_door=power_sliding_door)
        if auto_cruise_control is not None:
            cars = cars.filter(auto_cruise_control=auto_cruise_control)
        if price_min is not None:
            cars = cars.filter(price__gte=price_min)
        if price_max is not None:
            cars = cars.filter(price__lte=price_max)
        if instalment_min is not None:
            cars = cars.filter(instalment__gte=instalment_min)
        if instalment_max is not None:
            cars = cars.filter(instalment__lte=instalment_max)

    context = {
        'cars': cars,
        'form': form,
        'is_seller': user_profile.role == 'SEL',
        'is_buyer': user_profile.role == 'BUY',
        'is_admin': user_profile.role == 'ADM',
    }
    return render(request, 'car_list.html', context)

@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.role == 'SEL' and car.seller == request.user:
        car.delete()
        return redirect('product_catalog:car_list')
    elif user_profile.role == 'ADM':
        car.delete()
        return redirect('product_catalog:car_list')
    else:
        return redirect('authentication:login')

@login_required
def create_car(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.role != 'SEL': 
        return redirect('authentication:login')

    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user
            car.save()
            return redirect('product_catalog:car_list')
    else:
        form = CarForm()

    context = {
        'form': form,
    }
    return render(request, 'create_car.html', context)
