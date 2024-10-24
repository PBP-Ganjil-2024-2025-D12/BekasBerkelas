from django.urls import path
from review_rating.views import tes_review

app_name = 'review_rating'

urlpatterns = [
    path('tes_review/', tes_review, name='tes_review'),
]