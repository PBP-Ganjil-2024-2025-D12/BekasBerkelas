from django.urls import path
from forum.views import show_forum, create_question, create_reply, get_questions_json, forum_detail

app_name = 'forum'

urlpatterns = [
    path('', show_forum, name='show_forum'),
    path('create_question/', create_question, name='create_question'),
    path('<uuid:pk>/', forum_detail, name='forum_detail'),
    path('<uuid:pk>/create_reply/', create_reply, name='create_reply'),
    path('get_questions_json/', get_questions_json, name='get_questions_json'),
]