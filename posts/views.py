from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentModelForm


def post_list(request):
    posts = Post.objects.filter(status='published')
    return render(request, 'posts/post_list.html', context={'all_posts': posts})


def post_details(request, year, month, day, post_slug):
    try:
        post_detail = Post.objects.get(
            publish__year=year,
            publish__month=month,
            publish__day=day,
            slug=post_slug
        )

    except Post.DoesNotExist:
        return HttpResponse('<h1>Post not found</h1>')

    comments = Comment.objects.filter(post=post_detail, active=True)
    comment_form = CommentModelForm()
    context = {'post': post_detail, 'comments': comments, 'comment_form': comment_form}
    return render(request, 'posts/post_detail.html', context=context)


def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            comments = comment_form.save(commit=False)
            comments.post = post
            comments.save()
            context = {'post': post, 'comment': comments, 'form': comment_form}

            return render(request, 'posts/comment.html', context=context)

        else:
            (comment_form.errors)
