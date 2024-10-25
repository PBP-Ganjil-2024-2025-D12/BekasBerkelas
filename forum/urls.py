from django.urls import path
from forum.views import show_forum, create_question_ajax, create_reply_ajax, get_questions_json

app_name = 'forum'

urlpatterns = [
    path('', show_forum, name='show_forum'),
    path('create_question_ajax/', create_question_ajax, name='create_question_ajax'),
    path('create_reply/', create_reply_ajax, name='create_reply_ajax'),
    path('get-questions-json/', get_questions_json, name='get_questions_json'),
]