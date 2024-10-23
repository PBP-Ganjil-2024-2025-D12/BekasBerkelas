import datetime
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm
from jwt_auth.utils import set_jwt_cookies, clear_jwt_cookies

# Create your views here.
def register_user(request) :
    form = RegisterForm()
    access_token = request.COOKIES.get('access_token')
    
    if access_token :
        return redirect('main:main')
    
    if request.method == "POST" :
        form = RegisterForm(request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('authentication:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request) :
    access_token = request.COOKIES.get('access_token')
    if access_token :
        return redirect('main:main')
    
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        
        if user is not None :
            next = request.GET.get('next')
            if next is not None :
                response = redirect(next)
            else :
                response = redirect('main:main')
            return set_jwt_cookies(response, user)
        else :
            messages.error(request, 'Invalid username or password')
            return redirect('authentication:login')

    return render(request, 'login.html')

def logout_user(request) :
    response = redirect('authentication:login')
    return clear_jwt_cookies(response)