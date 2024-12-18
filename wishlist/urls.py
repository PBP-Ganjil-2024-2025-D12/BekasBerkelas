from django.urls import path
from wishlist.views import show_wishlist, add_to_wishlist, edit_wishlist, remove_from_wishlist, show_json

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='wishlist_page'),
    path('show_wishlist', show_wishlist, name='show_wishlist'),
    path('add/<uuid:car_id>', add_to_wishlist, name='add_to_wishlist'),
    path('edit/<uuid:wishlist_id>/', edit_wishlist, name='edit_wishlist'),
    path('remove/<uuid:wishlist_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('json/', show_json, name='show_json'),
]
