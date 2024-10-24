from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserRole

class RegisterForm(UserCreationForm) :
    name = forms.CharField(max_length = 300, required = True)
    email = forms.EmailField(required = True)
    no_telp = forms.CharField(max_length = 12, required = True)
    role = forms.ChoiceField(
        choices = UserRole.choices,
        initial = UserRole.BUYER,
        required = True
    )
    profile_picture = forms.ImageField(required = False)
    
    class Meta :
        model = User
        fields = ('username', 'name', 'email', 'no_telp', 'role', 'password1', 'password2')
    
    def save(self, commit=True) :
        user = super().save(commit = False)
        
        if commit :
            user.save()
            UserProfile.objects.create(
                user = user,
                name = self.cleaned_data['name'],
                email = self.cleaned_data['email'],
                no_telp = self.cleaned_data['no_telp'],
                role = self.cleaned_data['role'],
            ) 
        return user