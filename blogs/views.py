from django.http import HttpRequest
from django.shortcuts import get_list_or_404, get_object_or_404, render

from blogs.models import Post

# Create your views here.


def post_list(request: HttpRequest):
    posts = get_list_or_404(Post)
    return render(
        request=request, template_name="blogs/post/list.xhtml", context={"posts": posts}
    )


def post_detail(request: HttpRequest, pk: int):
    post = get_object_or_404(Post, id=pk)
    return render(
        request=request, template_name="blogs/post/detail.xhtml", context={"post": post}
    )
