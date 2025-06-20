from django import template
from django.db.models import Count

register = template.Library()


register = template.Library()


from blog.models import Post

register = template.Library()


@register.simple_tag
def total_posts() -> int:
    return Post.objects.count()


@register.inclusion_tag(filename="blog/post/latest_posts.html")
def show_latest_posts(count: int = 5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


# Simple tag that returns an QuerySet.
@register.simple_tag
def get_most_commented_posts(count: int = 5):
    return Post.published.annotate(total_comments=Count("comments")).order_by("-total_comments")[:count]
