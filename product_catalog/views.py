from django.shortcuts import render, redirect
from .models import Car
from django.contrib.auth.decorators import login_required
from .forms import CarForm, CarFilterForm
from authentication.models import UserProfile  # Adjust the import according to your app structure
from django.shortcuts import get_object_or_404
from wishlist.models import Wishlist
from django.http import JsonResponse
from user_dashboard.models import SellerProfile 



@login_required
def mobil_saya(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role == 'SEL':  # Replace 'seller' with the appropriate role value if needed
        cars = Car.objects.filter(seller=request.user)  # Fetch only the cars that belong to the seller
    else:
        return redirect('product_catalog:car_list')
    form = CarFilterForm(request.GET)
    user_wishlist = Wishlist.objects.filter(user=request.user).values_list('id', flat=True)

    if form.is_valid():
        # Standard filters
        car_name = form.cleaned_data.get('car_name')
        brand = form.cleaned_data.get('brand')
        year = form.cleaned_data.get('year')
        mileage = form.cleaned_data.get('mileage')
        location = form.cleaned_data.get('location')
        transmission = form.cleaned_data.get('transmission')
        plate_type = form.cleaned_data.get('plate_type')

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

        # Boolean filters - only filter when True
        if form.cleaned_data.get('rear_camera'):
            cars = cars.filter(rear_camera=True)
        if form.cleaned_data.get('sun_roof'):
            cars = cars.filter(sun_roof=True)
        if form.cleaned_data.get('auto_retract_mirror'):
            cars = cars.filter(auto_retract_mirror=True)
        if form.cleaned_data.get('electric_parking_brake'):
            cars = cars.filter(electric_parking_brake=True)
        if form.cleaned_data.get('map_navigator'):
            cars = cars.filter(map_navigator=True)
        if form.cleaned_data.get('vehicle_stability_control'):
            cars = cars.filter(vehicle_stability_control=True)
        if form.cleaned_data.get('keyless_push_start'):
            cars = cars.filter(keyless_push_start=True)
        if form.cleaned_data.get('sports_mode'):
            cars = cars.filter(sports_mode=True)
        if form.cleaned_data.get('camera_360_view'):
            cars = cars.filter(camera_360_view=True)
        if form.cleaned_data.get('power_sliding_door'):
            cars = cars.filter(power_sliding_door=True)
        if form.cleaned_data.get('auto_cruise_control'):
            cars = cars.filter(auto_cruise_control=True)

        # Range filters for price and installment
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')
        instalment_min = form.cleaned_data.get('instalment_min')
        instalment_max = form.cleaned_data.get('instalment_max')

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
            'user_wishlist': user_wishlist,
        }
        return render(request, 'mobil_saya.html', context)
    
@login_required   
def contact_seller(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
        seller_email = car.seller.userprofile.email
        seller_phone = car.seller.userprofile.no_telp
        data = {
            'email': seller_email,
            'phone': seller_phone,
        }
        return JsonResponse(data)
    except Car.DoesNotExist:
        return JsonResponse({'error': 'Car not found'}, status=404)
    
@login_required
def car_list(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role == 'SEL':  # Replace 'seller' with the appropriate role value if needed
        cars = Car.objects.filter(seller=request.user)  # Fetch only the cars that belong to the seller
    else:
        cars = Car.objects.all()
    form = CarFilterForm(request.GET)
    user_wishlist = Wishlist.objects.filter(user=request.user).values_list('id', flat=True)

    if form.is_valid():
        # Standard filters
        car_name = form.cleaned_data.get('car_name')
        brand = form.cleaned_data.get('brand')
        year = form.cleaned_data.get('year')
        mileage = form.cleaned_data.get('mileage')
        location = form.cleaned_data.get('location')
        transmission = form.cleaned_data.get('transmission')
        plate_type = form.cleaned_data.get('plate_type')

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

        # Boolean filters - only filter when True
        if form.cleaned_data.get('rear_camera'):
            cars = cars.filter(rear_camera=True)
        if form.cleaned_data.get('sun_roof'):
            cars = cars.filter(sun_roof=True)
        if form.cleaned_data.get('auto_retract_mirror'):
            cars = cars.filter(auto_retract_mirror=True)
        if form.cleaned_data.get('electric_parking_brake'):
            cars = cars.filter(electric_parking_brake=True)
        if form.cleaned_data.get('map_navigator'):
            cars = cars.filter(map_navigator=True)
        if form.cleaned_data.get('vehicle_stability_control'):
            cars = cars.filter(vehicle_stability_control=True)
        if form.cleaned_data.get('keyless_push_start'):
            cars = cars.filter(keyless_push_start=True)
        if form.cleaned_data.get('sports_mode'):
            cars = cars.filter(sports_mode=True)
        if form.cleaned_data.get('camera_360_view'):
            cars = cars.filter(camera_360_view=True)
        if form.cleaned_data.get('power_sliding_door'):
            cars = cars.filter(power_sliding_door=True)
        if form.cleaned_data.get('auto_cruise_control'):
            cars = cars.filter(auto_cruise_control=True)

        # Range filters for price and installment
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')
        instalment_min = form.cleaned_data.get('instalment_min')
        instalment_max = form.cleaned_data.get('instalment_max')

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
        'user_wishlist': user_wishlist,
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
    
    seller_profile = SellerProfile.objects.get(user_profile=user_profile)

    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user
            car.seller_buat_dashboard  = seller_profile
            car.save()
            return redirect('product_catalog:mobil_saya')
        else:
            print(form.errors)  # This will log any validation errors

    else:
        form = CarForm()

    context = {
        'form': form,
    }
    return render(request, 'create_car.html', context)