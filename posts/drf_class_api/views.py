from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Post
from .serializers import PostSerializer, PostWithContentSerializer, PostTitleSerializer, SharePostSerializer


class PostListView(APIView):
    def get(self, request):
        posts = Post.published.all()
        serializer = PostSerializer(instance=posts, many=True)
        data = serializer.data
        return Response(data, status=200)


class PostCreateView(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            resp = {"message": "Post created successfully", "status": "success", "data": serializer.data}
            return Response(resp, status=201)
        return Response(serializer.errors, status=400)


# class PostApiView(APIView):
#     def get_object(self, post_id):
#         try:
#             return Post.objects.get(id=post_id)
#         except Post.Doesnotexist:
#             return Response({"message": "Post not found"}, status=400)
#     def get(self, request, post_id):
