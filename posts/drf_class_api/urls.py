from django.urls import path
from .views import PostListView

app_name = 'drf_class_api'
urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts_class_api')

]
