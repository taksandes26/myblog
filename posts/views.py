from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentModelForm,EmailPostForm
from django.core.paginator import Paginator,PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Q


def post_list(request):
    posts = Post.objects.filter(status='published')

    try:
        posts_per_page = 3
        paginator = Paginator(object_list=posts,per_page=posts_per_page)
        page_number = request.GET.get('page',1)
        page_obj = paginator.page(page_number)
        return render(request, 'posts/post_list.html', context={'page_obj':page_obj, 'all_posts': posts})

    except PageNotAnInteger:
        page_obj = paginator.page(1)



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

def share_post(request, post_id):
    post=get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        sent = False # sent variable to track whether the email has been sent.
        if form.is_valid():
            cd = form.cleaned_data #dictionary of cleaned data from EmailPostForm If the form is valid, extract the cleaned data from the form.
            post_url = request.build_absolute_uri(post.get_absolute_url()) # Generate the absolute URL which  included in the email.
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject=subject,message=message,from_email=cd['email'], recipient_list=[cd['to']])
            sent = True
            return render(request,'posts/share.html',context={'post':post,'form':form,'sent':sent})
        else:
            print(form.errors)
            return HttpResponse('Invalid form')

    else:
        form = EmailPostForm()
        return render(request, 'posts/share.html', context={'post': post, 'form': form})


def search_post(request):
    query = request.GET.get('query')
    searched_post = Post.objects.filter(
        Q(title__icontains=query)|Q(content__icontains=query)|
        Q(author__username__icontains=query)
    ).distinct()
    return render(request,'posts/search.html',context={'posts':searched_post,'query':query})
