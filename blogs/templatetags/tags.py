from django.db.models import Count
from django.template import Library
from django.utils.safestring import mark_safe
from markdown import markdown

from blogs.models import Post

register: Library = Library()


@register.simple_tag
def total_posts():
    return Post.objects.all().count()


@register.inclusion_tag(filename="blogs/post/latest_posts.xhtml")
def latest_posts(count: int = 5):
    return {"latest_posts": Post.objects.filter().order_by("-publish")[:count]}


@register.simple_tag
def get_most_commented_posts(count: int = 5):
    return (
        Post.objects.all()
        .annotate(total_comments=Count("comments"))
        .order_by("-total_comments")[:count]
    )


@register.filter(name="markdown")
def markdown_format(text: str):
    return mark_safe(markdown(text))
