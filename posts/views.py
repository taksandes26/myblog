from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .models import Post, Comment


def post_list(request):
    posts = Post.objects.filter(status='published')
    return render(request, 'posts/post_list.html', context={'all_posts': posts})


def post_details(request, year, month, day, post_slug):
    post_detail = Post.objects.get(
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post_slug
    )

    return render(request, 'posts/post_detail.html', context={'post': post_detail})


def post_comment(request):
    if request.method == "POST":
        data = request.POST
        post = Post.objects.get(id=data['post_id'])
    #  comment=Comment(post=post,name=data['name'],email=data['email'],content=data['comment'])
    #  comment.save()
    Comment.objects.create(post_id=data['post_id'], name=data['name'], email=data['email'], content=data['comment'])
    comments = Comment.objects.filter(post=post)

    return render(request, 'posts/post_detail.html', context={'post': post, 'comments': comments})
