from django.template import Library

from blogs.models import Post

register: Library = Library()


@register.simple_tag
def total_posts():
    return Post.objects.all().count()


@register.inclusion_tag(filename="blogs/post/latest_posts.xhtml")
def latest_posts(count: int = 5):
    return {"latest_posts": Post.objects.filter().order_by("-publish")[:count]}
