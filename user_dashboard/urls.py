from django.urls import path
from user_dashboard.views import user_dashboard, user_biodata, upload_profile_picture, change_password, update_profile, product_list

app_name = 'dashboard'

urlpatterns = [
    path('', user_dashboard, name='dashboard'),
    path('biodata/', user_biodata, name='biodata'),
    path('biodata/upload_profile_picture/', upload_profile_picture, name='upload_profile_picture'),
    path('biodata/change_password', change_password,  name="change_password"),
    path('biodata/update_profile', update_profile,  name="update_profile"),
    path('product-list/', product_list, name="product_list" )
]