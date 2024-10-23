from django.urls import path
from main.views import main
from wishlist.views import add_to_wishlist, show_wishlist, remove_from_wishlist

app_name = 'main'

urlpatterns = [
    path('', main, name='main'),
    path('', show_wishlist, name='wishlist_page'),
    path('add/<int:car_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:car_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]