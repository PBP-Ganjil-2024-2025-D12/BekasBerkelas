from django.shortcuts import render, redirect
from authentication.models import UserProfile, UserRole
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from bekas_berkelas import settings
from django.contrib.auth import update_session_auth_hash
import os
import uuid

# Create your views here.
def user_dashboard(request) :
    return redirect(reverse("dashboard:biodata"))

@login_required
def user_biodata(request) :
    user = request.user
    user_profile = UserProfile.objects.get(user = user)
    user_role = user_profile.role

    if user_role == UserRole.BUYER :
        context = {'base': 'base_buyer_dashboard.html'}
        template = 'biodata.html'
    elif user_role == UserRole.SELLER:
        context = {'base': 'base_seller_dashboard.html'}
        template = 'biodata.html'
    elif user_role == UserRole.ADMIN:
        context = {'dashboard': 'base_admin_dashboard.html'}
        template = 'admin_dashboard.html'
    else:
        redirect(reverse("auth:login"))

    return render(request, template, context)


@login_required
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES['profile_picture']:
        profile = request.user.userprofile
        profile_picture = request.FILES['profile_picture']

        if profile.profile_picture:
            old_file_path = os.path.join(settings.MEDIA_ROOT, profile.profile_picture.path)
            
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        new_filename = f"{uuid.uuid4()}.{profile_picture.name.split('.')[-1]}"
        profile_picture.name = new_filename

        profile.profile_picture = profile_picture
        profile.save()
        messages.success(request, 'Profile picture uploaded successfully!')

    return redirect(reverse("dashboard:biodata"))

@login_required
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