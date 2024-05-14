from django.urls import path

from . import views
from .views import post_list, post_details, post_comment

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', post_details, name='post_details'),
    path('post-comment/', post_comment, name='post_comment')
]
