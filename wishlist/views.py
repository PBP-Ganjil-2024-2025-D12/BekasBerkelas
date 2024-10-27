from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
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
            wishlist_item, created = Wishlist.objects.get_or_create(user=user, car=car, defaults={'priority':'1'})
            
            if created:
                return JsonResponse({'status': 'success','action': 'added','message': 'Menambahkan ke wishlist'})
            else:
                wishlist_item.delete()
                return JsonResponse({'status': 'success','action': 'removed','message': 'Menghapus dari wishlist'})
                
        except Exception as e:
            return JsonResponse({'status': 'error','message': f'Error with wishlist operation: {str(e)}'}, status=500)
            
    except Exception as e:
        return JsonResponse({'status': 'error','message': str(e)}, status=500)

@login_required(login_url='/auth/login')
def show_wishlist(request):
    priority_filter = request.GET.get('priority', None)
    wishlists = Wishlist.objects.filter(user=request.user)
    
    if priority_filter:
        wishlists = wishlists.filter(priority=priority_filter)
        
    context = {'wishlists': wishlists, 'selected_priority': priority_filter, 'priority_choices': Wishlist.PRIORITY_CHOICES}
    return render(request, 'wishlist.html', context)


@login_required(login_url='/auth/login')
def edit_wishlist(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    
    if request.method == 'POST':
        priority_map = {'Rendah': 1, 'Sedang': 2, 'Tinggi': 3}
        new_priority = request.POST.get('priority')
        wishlist.priority = priority_map.get(new_priority, 1)
        wishlist.save()
        return redirect('wishlist:show_wishlist')
    
    return render(request, 'edit_wishlist.html', {'wishlist': wishlist})


@require_http_methods(["POST"])
@login_required(login_url='/auth/login')
def remove_from_wishlist(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist.delete()
    return HttpResponseRedirect(reverse('wishlist:show_wishlist'))

