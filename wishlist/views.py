from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Wishlist
from product_catalog.models import Car
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["POST"])
@login_required(login_url='/login')
def add_to_wishlist(request):
    try:
        data = json.loads(request.body)
        car_id = data.get('car_id')
        
        if not car_id:
            return JsonResponse({'message': 'Car ID is required'}, status=400)
            
        car = get_object_or_404(Car, id=car_id)
        user_profile = request.user.userprofile
        wishlist_item, created = Wishlist.objects.get_or_create(user=user_profile, car=car)
        
        if created:
            return JsonResponse({'status': 'added', 'message': 'Car added to wishlist'})
        else:
            wishlist_item.delete()
            return JsonResponse({'status': 'removed', 'message': 'Car removed from wishlist'})
            
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


@login_required(login_url='/login')
def show_wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlists': wishlists
    }
    return render(request, 'wishlist.html', context)

@login_required(login_url='/login')
@require_http_methods(["POST"])
def remove_from_wishlist(request, pk):
    try:
        wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user)
        wishlist.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Wishlist item deleted successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
