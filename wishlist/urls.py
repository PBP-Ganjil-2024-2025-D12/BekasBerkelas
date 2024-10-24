from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.show_wishlist, name='wishlist_page'),
    path('add/<int:car_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:car_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
