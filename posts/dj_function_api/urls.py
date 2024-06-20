from django.urls import path
from .views import post_list_api, post_with_comment_api, list_comment_api

app_name = 'posts'
urlpatterns = [
    path('v1/posts/',post_list_api, name='post_list_api')
]