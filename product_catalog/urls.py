from django.urls import path
from product_catalog.views import car_list, create_car, delete_car

app_name = 'product_catalog'

urlpatterns = [
    path('car_list/', car_list, name='car_list'),  # For listing cars
    path('create_car/', create_car, name='create_car'),  # For creating a new car
    path('delete_car/<int:car_id>/', delete_car, name='delete_car'),
]
