from django.urls import path
from wishlist.views import show_wishlist, add_to_wishlist, update_wishlist, remove_from_wishlist

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='wishlist_page'),
    path('add/<uuid:car_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('update/<uuid:car_id>/', update_wishlist, name='update_wishlist'),
    path('remove/<uuid:car_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
