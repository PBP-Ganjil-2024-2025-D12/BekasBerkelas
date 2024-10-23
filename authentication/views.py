import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.
def register_user(request) :
    form = RegisterForm()
    
    if request.user.is_authenticated :
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
    if request.user.is_authenticated :
        return redirect('main:main')
    
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        
        if user is not None :
            login(request, user)
            next = request.GET.get('next')
            if next is not None :
                response = redirect(next)
            else :
                response = redirect('main:main')
            response.set_cookie('user_login', user)
            return response
        else :
            messages.error(request, 'Invalid username or password')
            return redirect('authentication:login')

    return render(request, 'login.html')

def logout_user(request) :
    logout(request)
    response = redirect('authentication:login')
    response.delete_cookie('user_login')
    return response