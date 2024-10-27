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
        wishlist_item, created = Wishlist.objects.get_or_create(user=user_profile, car=car, defaults={'priority':'1'})
        
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
    priority_filter = request.GET.get('priority', None)
    wishlists = Wishlist.objects.filter(user=request.user)
    
    if priority_filter:
        wishlists = wishlists.filter(priority=priority_filter)
        
    context = {
        'wishlists': wishlists,
        'selected_priority': priority_filter,
        'priority_choices': Wishlist.PRIORITY_CHOICES
    }
    return render(request, 'wishlist.html', context)


@login_required(login_url='/login')
def edit_wishlist(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user.userprofile)
    
    if request.method == 'POST':
        new_priority = request.POST.get('priority')
        wishlist.priority = new_priority
        wishlist.save()
        return redirect('wishlist:show_wishlist')
    
    return render(request, 'edit_wishlist.html', {'wishlist': wishlist})


@require_http_methods(["POST"])
@login_required(login_url='/login')
def remove_from_wishlist(request, wishlist_id):
    try:
        wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user.userprofile)
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

