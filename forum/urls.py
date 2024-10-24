from django.urls import path
from forum.views import show_forum, create_question_ajax, create_reply_ajax

app_name = 'forum'

urlpatterns = [
    path('', show_forum, name='show_forum'),
    path('create_forum/', create_question_ajax, name='create_question_ajax'),
    path('reply/', create_reply_ajax, name='create_reply_ajax'),
]