from django.shortcuts import render, redirect
from .models import Car
from django.contrib.auth.decorators import login_required
from .forms import CarForm
from authentication.models import UserProfile  # Adjust the import according to your app structure
from django.shortcuts import get_object_or_404

@login_required
def car_list(request):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        
        if user_profile.role == 'BUY':
            # Buyer: show all cars
            cars = Car.objects.all()
            is_seller = False
            is_admin = False
        elif user_profile.role == 'SEL':
            # Seller: show only the cars they sell
            cars = Car.objects.filter(seller=request.user)
            is_seller = True
            is_admin = False
        elif user_profile.role == 'ADM':
            # Admin: show all cars
            cars = Car.objects.all()
            is_seller = False
            is_admin = True
        else:
            # Default redirect if no valid role
            return redirect('authentication:login')

        context = {
            'cars': cars,
            'is_seller': is_seller,
            'is_admin': is_admin,
        }
        return render(request, 'car_list.html', context)

@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Check if the user is a seller or an admin
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
    # Get the user's profile
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.role != 'SEL':  # Adjust role check to match your choices
        return redirect('authentication:login')

    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            # Automatically assign the seller (user) to the car
            car = form.save(commit=False)
            car.seller = request.user
            car.save()
            return redirect('product_catalog:car_list')  # Make sure to use the correct URL name
    else:
        form = CarForm()

    context = {
        'form': form,
    }
    return render(request, 'create_car.html', context)
