from ..models import Post, Comment
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'status', 'publish', 'author']


class PostWithContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content']


class PostTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title']


class SharePostSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    to = serializers.EmailField()
    comments = serializers.CharField(required=False, allow_blank=True)
