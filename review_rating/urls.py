from django.urls import path
from review_rating.views import show_profile, add_review, show_json

app_name = 'review_rating'

urlpatterns = [
    path('<str:username>/', show_profile, name='show_profile'),
    path('<str:username>/add_review/', add_review, name='add_review'),
    path('<str:username>/show_json/', show_json, name='show_json'),
]