from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from product_catalog.models import Car

@login_required(login_url='/login')
def add_to_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == "POST":
        exisiting_item = Wishlist.objects.filter(user=request.user, car=car).exists()
        
        if not exisiting_item:
            wishlist_item = Wishlist(User=request.user, car=car)
            wishlist_item.save()
            return redirect("wishlist.html")
        
    return redirect("product_catalog.html")

@login_required(login_url='/login')
def show_wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist' : wishlists})

@login_required(login_url='/login')
def remove_from_wishlist(request, car_id):
    wishlist_item = get_object_or_404(Wishlist, user=request.user, car_id=car_id)
    wishlist_item.delete()
    return redirect('wishlist_page')