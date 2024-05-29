from django.urls import path

from . import views
from .views import post_list, post_details, post_comment, share_post, search_post

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', post_details, name='post_details'),
    path('<int:post_id>/comment/', post_comment, name='post_comment'),
    path('<int:post_id>/share/', share_post, name='share_post'),
    path('search/', search_post, name='search_post')
]
