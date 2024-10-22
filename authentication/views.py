import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from .forms import RegisterForm

# Create your views here.
def register(request) :
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

def login(request) :
    if request.user.is_authenticated :
        return redirect('main:main')
    
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        
        if user is not None :
            login(request, user)
            # TODO : Implement next page if user click a menu while not login
            response = HttpResponseRedirect(reverse("main:main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else :
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def logout(request) :
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:login'))
    response.delete_cookie('last_login') # Implement JWT
    return response