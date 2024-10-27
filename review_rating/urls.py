from django.urls import path
from review_rating.views import show_profile, add_review, show_json, show_reviews

app_name = 'review_rating'

urlpatterns = [
    path('<str:username>/', show_profile, name='show_profile'),
    path('<str:username>/add_review/', add_review, name='add_review'),
    path('<str:username>/show_json/', show_json, name='show_json'),
    path('<str:username>/reviews/', show_reviews, name='show_reviews'),
]