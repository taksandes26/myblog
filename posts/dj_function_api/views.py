from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view

from posts.models import Post, Comment
from django.core import serializers


def post_list_api(request):  # request parameter represents the HTTP request sent to the server.
    """
    This function is used to return all posts in JSON format
    Consistency: Using a consistent key ('posts') ensures that the API response structure is predictable.
    Clients consuming this API will always know where to find the list of posts in the response.
    data = {'posts': list(posts.values())}
    This makes it easy for clients to parse and understand the returned data,
    knowing exactly where to find posts based on the key.
    """
    # # The Post model likely represents a database table containing posts.
    posts = Post.objects.all()
    # This is a Django QuerySet method that retrieves all records from the Post table in
    # the database.
    # Serialize
    data = {'posts': list(posts.values())}
    return JsonResponse(data, status=200)


def post_with_comment_api(request):
    posts = Post.objects.all()
    data = []
    for post in posts:
        comments = post.comments.filter(active=True)
        data.append({"post": post.title, "comments": list(comments.values('name', 'email', 'content'))})
    return JsonResponse(data, status=200, safe=False)


@api_view
def list_comment_api(request):
    comments = Comment.objects.all()
    data = serializers.serialize(format='json', query_set=comments)
    return HttpResponse(content=data, status=200, content_type='application/jason')
