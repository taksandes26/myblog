from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Post
from .serializers import PostSerializer


class PostListView(APIView):
    def get(self, request):
        posts = Post.published.all()
        serializer = PostSerializer(instance=posts, many=True)
        data = serializer.data
        return Response(data, status=200)
