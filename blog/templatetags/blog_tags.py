from django import template

from blog.models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.count()


@register.inclusion_tag
def a():
    pass
