from django.shortcuts import render, redirect
from authentication.models import UserProfile, UserRole
from review_rating.models import ReviewRating
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http import JsonResponse
from django.templatetags.static import static
import cloudinary.uploader
import json
from django.core.paginator import Paginator

# Create your views here.
def user_dashboard(request) :
    return redirect("dashboard:biodata")

@login_required(login_url='/auth/login')
def user_biodata(request) :
    user = request.user
    user_profile = UserProfile.objects.get(user = user)
    user_role = user_profile.role

    if user_role == UserRole.BUYER or user_role == UserRole.SELLER or user_role == UserRole.ADMIN  :
        return render(request, 'biodata.html', {})
    else:
        return redirect('/auth/login')


@login_required(login_url='/auth/login')
def upload_profile_picture(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        profile_picture_url = request.POST["profile_picture_url"]
        profile_picture_id = request.POST["profile_picture_id"]
        

        if profile.profile_picture_id:
            cloudinary.uploader.destroy(profile.profile_picture_id)

        profile.profile_picture = profile_picture_url
        profile.profile_picture_id = profile_picture_id

        profile.save()
        messages.success(request, 'Profile picture uploaded successfully!')

    return redirect("dashboard:biodata")

@login_required(login_url='/auth/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Tetap login setelah password diubah
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard:biodata')  # Redirect setelah sukses
        else:
            messages.error(request, 'There was an error updating your password. Please try again.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'change_password.html', {'form': form})

@login_required(login_url='/auth/login')
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
            email = strip_tags(request.POST.get('email'))
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


@login_required(login_url='/auth/login')
def rating_list(request):

    if request.user.userprofile.role != 'SEL':
        return redirect('/dashboard')
    
    daftar_review = {}
    if not request.user.userprofile.sellerprofile.reviews_received.exists():
        has_review = False
    else :
        daftar_review_seller = request.user.userprofile.sellerprofile.reviews_received.all()
        has_review = True

        page_number = request.GET.get('page', 1)
        paginator = Paginator(daftar_review_seller, 10)
        page_obj = paginator.get_page(page_number)

        for review in page_obj.object_list:

            if not review.reviewer.user_profile.profile_picture:
                reviewer_profile = static('user_dashboard/image/default-profile.png')
            else:
                reviewer_profile = review.reviewer.user_profile.profile_picture

            print(reviewer_profile)

            daftar_review[str(review.id)] = {
                'review' : review.review,
                'rating' : review.rating,
                'reviewer' : review.reviewer.user_profile.name,
                'reviewer_profile_pic' : reviewer_profile 
            }

    context = {
        'has_review' : has_review,
        'daftar_review' : daftar_review,
        'page_obj' : page_obj
    }

    return render(request, 'seller_rating_list.html', context)

@login_required(login_url='/auth/login')
def verifikasi_penjual(request):
    if request.user.userprofile.role != 'ADM':
        return redirect('/dashboard')
    
    if request.method == 'POST':
        try:
            verified_seller = UserProfile.objects.get(id=request.POST["idUser"])
            verified_seller.is_verified = True
            verified_seller.save()
            messages.success(request,"Berhasil Verifikasi Penjual")
            return redirect("dashboard:verifikasi_penjual")
        except:
            messages.error(request,"Gagal Verifikasi Penjual")
            return redirect("dashboard:verifikasi_penjual")

    unverified_seller_query = UserProfile.objects.filter(role='SEL', is_verified=False)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(unverified_seller_query, 10)
    page_obj = paginator.get_page(page_number)
    
    if not unverified_seller_query.exists():
        unverified_seller = None
    else:
        page_number = request.GET.get('page')

        default_profile_pic = static('user_dashboard/image/default-profile.png')
        unverified_seller = {}

        for seller in page_obj.object_list:
            if not seller.profile_picture:
                seller_profile_picture = default_profile_pic
            else:
                seller_profile_picture =  seller.profile_picture

            unverified_seller[seller.id] = {
                'nama' : seller.name,
                'email' : seller.email,
                'profile_pic' : seller_profile_picture
            }

    context = {
        'unverified_seller' : unverified_seller,
        'page_obj' : page_obj
    }

    return render(request, 'adm_verifikasi_penjual.html', context)

@login_required(login_url='/auth/login')
@csrf_exempt
@require_POST
def get_user(request):
    try:
        data = json.loads(request.body)
        user = UserProfile.objects.get(id=data["id"])
        if not user.profile_picture:
            profile_pic = static('user_dashboard/image/default-profile.png')
        else:
            profile_pic = user.profile_picture

        if not user.is_verified:
            status = 'Menunggu Verifikasi'
        else:
            status = 'Sudah Verifikasi'

        return JsonResponse({
            'id' : user.id,
            'nama' : user.name,
            'email' : user.email,
            'no_telp' : user.no_telp,
            'role' : user.role,
            'profile_picture' : profile_pic,
            'status' : status,
        })
    except:
        return JsonResponse({"error": "User not found"}, status=404)
