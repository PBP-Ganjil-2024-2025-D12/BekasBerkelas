from django.shortcuts import render, redirect
from authentication.models import UserProfile, UserRole
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from bekas_berkelas import settings
from django.contrib.auth import update_session_auth_hash
import os
import uuid
import cloudinary.uploader
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http import JsonResponse

# Create your views here.
def user_dashboard(request) :
    return redirect(reverse("dashboard:biodata"))

@login_required(login_url=reverse_lazy('authentication:login')) # Handle Circular Import
def user_biodata(request) :
    user = request.user
    user_profile = UserProfile.objects.get(user = user)
    user_role = user_profile.role

    if user_role == UserRole.BUYER or user_role == UserRole.SELLER or user_role == UserRole.ADMIN  :
        return render(request, 'biodata.html', {})
    else:
        return redirect(reverse_lazy("authentication:login"))


@login_required(login_url=reverse_lazy('authentication:login'))
def upload_profile_picture(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        profile_picture_url = request.POST["profile_picture_url"]
        profile_picture_id = request.POST["profile_picture_id"]
        

        if profile.profile_picture_id:
            result = cloudinary.uploader.destroy(profile.profile_picture_id)

        profile.profile_picture = profile_picture_url
        profile.profile_picture_id = profile_picture_id

        profile.save()
        messages.success(request, 'Profile picture uploaded successfully!')

    return redirect(reverse("dashboard:biodata"))

@login_required(login_url=reverse_lazy('authentication:login'))
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Tetap login setelah password diubah
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse('dashboard:biodata'))  # Redirect setelah sukses
        else:
            messages.error(request, 'There was an error updating your password. Please try again.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'change_password.html', {'form': form})

@login_required(login_url=reverse_lazy('authentication:login'))
@csrf_exempt
@require_POST
def update_profile(request):
    if request.method == 'POST':
        user_profile = request.user.userprofile

        if 'name' in request.POST:
            user_profile.name = strip_tags(request.POST.get('name'))
            data = user_profile.name
        
        
        if 'email' in request.POST:
            validator = EmailValidator()
            email = request.POST.get('email')
            try:
                validator(email)
                user_profile.email = email
                data = user_profile.email
            except ValidationError:
                return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

        if 'no_telp' in request.POST:
            user_profile.no_telp = strip_tags(request.POST.get('no_telp'))
            data = user_profile.no_telp

        # Simpan perubahan yang dilakukan
        user_profile.save()

        return JsonResponse({'status': 'success', 'message': 'Profile updated successfully', 'data': data})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required(login_url=reverse_lazy('authentication:login'))
def product_list(request):
    return render(request, 'seller_product_list.html', {})
