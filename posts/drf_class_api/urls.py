from django.urls import path
from .views import PostListView, PostCreateView

app_name = 'drf_class_api'
urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts_class_api'),
    path('create_post/', PostCreateView.as_view(), name='create_post_api')

]
