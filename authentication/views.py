from django.shortcuts import render, redirect, reverse
from .forms import UserForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def register(request) :
    form = UserCreationForm()
    
    if request.method == "POST" :
        form = UserCreationForm(request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('authentication:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login(request) :
    if request.method == 'POST' :
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid() :
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse('main:main'))
            return response
        else :
            messages.error(request, "Invalid username or password. Please try again!")
    
    else :
        form = AuthenticationForm(request)
    context = {'form':form}
    return render(request, 'login.html', context)

def logout(request) :
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:login'))
    
    return response