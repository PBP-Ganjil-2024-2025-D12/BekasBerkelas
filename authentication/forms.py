from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserRole

class RegisterForm(UserCreationForm) :
    name = forms.CharField(max_length = 300, required = True)
    email = forms.EmailField(required = True)
    role = forms.ChoiceField(
        choices = UserRole.choices,
        initial = UserRole.BUYER,
        required = True
    ) # TODO : Implement if role admin, they must input admin hash password to create account!
    profile_picture = forms.ImageField(required = False)
    
    class Meta :
        model = User
        fields = ('username', 'name', 'email', 'role', 'password1', 'password2')
    
    def save(self, commit=True) :
        user = super().save(commit = False)
        
        if commit :
            user.save()
            UserProfile.objects.create(
                user = user,
                name = self.cleaned_data['name'],
                email = self.cleaned_data['email'],
                role = self.cleaned_data['role'],
            ) 
        return user