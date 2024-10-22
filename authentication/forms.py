from django.forms import ModelForm
from django.utils.html import strip_tags
from main.models import UserProfile

class UserForm(ModelForm) :
    class Meta :
        model = UserProfile
        fields = ["name", "email", "profile_picture"]
    
    def clean_name(self) :
        name = self.cleaned_data["name"]
        return strip_tags(name)
    
    def clean_price(self) :
        email = self.cleaned_data["email"]
        return strip_tags(email)
    
    def clean_profile_picture(self) :
        profile_picture = self.cleaned_data["profile_picture"]
        return strip_tags(profile_picture)