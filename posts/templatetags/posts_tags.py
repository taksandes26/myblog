from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("posts/latest_posts.html")
def show_latest_post(count=3):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count=3):
    posts = Post.published.annotate(total_comments=Count('comments')).order_by("-total_comments")[:count]
    return posts


@register.filter
def my_filter(input_text):
    return f"filtered posts {input_text}"
