from django.urls import path
from main.views import main
from wishlist.views import add_to_wishlist, show_wishlist, remove_from_wishlist

app_name = 'main'

urlpatterns = [
    path('', main, name='main'),
]