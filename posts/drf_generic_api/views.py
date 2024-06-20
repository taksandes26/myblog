from rest_framework import generics
from .serializers import PostSerializer
from ..models import Post


class PostListApiView(generics.ListAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer


class PostCreateApiView(generics.CreateAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer
