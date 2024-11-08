from django import template
from django.utils.safestring import mark_safe
from markdown import markdown

from blog.models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count: int = 5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.filter(name="markdown")
def markdown_format(text: str):
    return mark_safe(markdown(text=text))
