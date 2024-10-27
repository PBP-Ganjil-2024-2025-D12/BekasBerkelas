from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Wishlist
from product_catalog.models import Car
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["POST"])
@login_required(login_url='/auth/login')
def add_to_wishlist(request, car_id):
    try:
        car = get_object_or_404(Car, id=car_id)
        user = request.user
            
        try:
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                car=car, 
                defaults={'priority':'1'}
            )
            
            if created:
                print("Created new wishlist item")
                return JsonResponse({'status': 'success','action': 'added','message': 'Car added to wishlist'})
            else:
                print("Removing existing wishlist item")
                wishlist_item.delete()
                return JsonResponse({'status': 'success','action': 'removed','message': 'Car removed from wishlist'})
                
        except Exception as e:
            print(f"Error with wishlist operation: {str(e)}")
            return JsonResponse({'status': 'error','message': f'Error with wishlist operation: {str(e)}'}, status=500)
            
    except Exception as e:
        print(f"Main error: {str(e)}")
        return JsonResponse({'status': 'error','message': str(e)}, status=500)

@login_required(login_url='/auth/login')
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


@login_required(login_url='/auth/login')
def edit_wishlist(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    
    if request.method == 'POST':
        priority_map = {
            'LOW': 1,
            'MEDIUM': 2,
            'HIGH': 3
        }
        new_priority = request.POST.get('priority')
        wishlist.priority = priority_map.get(new_priority, 1)  # Default to 1 if invalid priority
        wishlist.save()
        return redirect('wishlist:show_wishlist')
    
    return render(request, 'edit_wishlist.html', {'wishlist': wishlist})


@require_http_methods(["POST"])
@login_required(login_url='/auth/login')
def remove_from_wishlist(request, wishlist_id):
    try:
        wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
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

