from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from review_rating.models import ReviewRating
from user_dashboard.models import UserProfile, SellerProfile, BuyerProfile, AdminProfile
from product_catalog.models import Car
from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required(login_url='/auth/login')
def show_profile(request, username):
    seller = get_object_or_404(SellerProfile, user_profile=UserProfile.objects.get(user=User.objects.get(username=username)))
    reviews = ReviewRating.objects.filter(reviewee=seller)
    cars = Car.objects.filter(seller_buat_dashboard=seller)
    context = {
        'seller': seller,
        'cars' : cars,
        'reviews': reviews
    }
    return render(request, "seller_profile.html", context)

@csrf_exempt
@require_POST
@login_required(login_url='/auth/login')
def add_review(request, username):
    try:
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.role != 'BUY':
            return JsonResponse({'error': 'You must be a buyer to leave a review.'}, status=403)
        
        review = request.POST.get("review")
        rating = request.POST.get("rating")
        reviewee_username = username

        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid rating format'}, status=400)

        reviewer = BuyerProfile.objects.get(user_profile=user_profile)

        if not all([review, rating, reviewee_username]):
            return JsonResponse({'error': 'All fields are required'}, status=400)

        try:
            reviewee = SellerProfile.objects.get(user_profile__user__username=reviewee_username)
        except SellerProfile.DoesNotExist:
            return JsonResponse({'error': 'Invalid reviewee'}, status=400)

        new_review_rating = ReviewRating(
            review=review,
            rating=rating,
            reviewer=reviewer,
            reviewee=reviewee
        )
        new_review_rating.save()

        average_rating = ReviewRating.objects.filter(reviewee=reviewee).aggregate(Avg('rating'))['rating__avg']

        reviewee.rating = average_rating
        reviewee.save()

        return JsonResponse({'message': 'Review created successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def show_json(request, username):
    seller = get_object_or_404(SellerProfile, user_profile=UserProfile.objects.get(user=User.objects.get(username=username)))
    reviews = ReviewRating.objects.filter(reviewee=seller)
    return HttpResponse(serializers.serialize("json", reviews), content_type="application/json")