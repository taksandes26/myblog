from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentModelForm, EmailPostForm, SearchForm
from django.core.paginator import Paginator, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Q
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count


def post_list(request, tag_slug=None):

    posts = Post.objects.filter(status='published')
    paginator = None
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    try:
        posts_per_page = 3
        paginator = Paginator(object_list=posts,per_page=posts_per_page)
        page_number = request.GET.get('page',1)
        page_obj = paginator.page(page_number)

    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except Empty_page:
        page_obj = paginator.page(paginator.num_pages)

    latest = Post.get_latest_post()
    post_count = 3
    latest_post = Post.objects.filter(status='published').order_by('-publish')[:post_count]

    published_post = Post.objects.filter(status='published')
    most_commented_post = published_post.annotate(total_comments=Count('comments')).order_by('-total_comments')[:post_count]

    return render(
        request,
        'posts/list.html',
        context={'posts': page_obj,'tag':tag,'latest_posts':latest_post,'most_commented_posts':most_commented_post})





def post_detail(request, year, month, day, post_slug):
    try:
        post_detail = Post.objects.get(
            publish__year=year,
            publish__month=month,
            publish__day=day,
            slug=post_slug
        )

    except Post.DoesNotExist:
        return render(request,'404.html')

    comments = Comment.objects.filter(post=post_detail, active=True)
    comment_form = CommentModelForm()
    post_list = 4
    post_tags_ids = post_detail.tags.values_list("id",flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post_detail.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags','-publish')[:post_list]
    context = {"post":post_detail,"comments":comments,"form":comment_form,"similar_posts":similar_posts}
    return render(request,'posts/detail.html',context=context)
@require_POST
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
    search_form = SearchForm()

    if 'query' in  request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Post.published.filter(
            Q(title__icontains=query)|Q(content__icontains=query)|
            Q(author__username__icontains=query)
            ).distinct()
            return render(request,'posts/search.html',context={'results':results,'query':query})
    else:
        return render(request,'posts/search.html',context={'form':search_form})
