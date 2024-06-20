from django.urls import path
from .views import PostListApiView, PostCreateApiView

app_name = "drf_generic_api"

urlpatterns = [
    path('posts/', PostListApiView.as_view(), name='posts_api'),
    path('create_posts/', PostCreateApiView.as_view(), name='create_posts'),
]
