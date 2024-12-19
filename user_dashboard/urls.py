from django.urls import path
from user_dashboard import views


app_name = 'dashboard'

urlpatterns = [
    path('', views.user_dashboard, name='dashboard'),
    path('biodata/', views.user_biodata, name='biodata'),
    path('biodata/upload_profile_picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('biodata/change_password/', views.change_password,  name="change_password"),
    path('biodata/update_profile/', views.update_profile,  name="update_profile"),
    path('rating_list/', views.rating_list, name="rating_list" ),
    path('verifikasi_penjual/', views.verifikasi_penjual, name="verifikasi_penjual" ),
    path('get_user/', views.get_user, name="get_user"),
    path('get_user_flutter/', views.get_user_flutter, name="get_user_flutter"),
    path('update_profile_flutter/', views.update_profile_flutter, name="update_profile_flutter")
]