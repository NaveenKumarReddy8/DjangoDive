from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from blog.models import Post

# Create your views here.


def post_list(request: HttpRequest):
    posts = Post.published.all()
    return render(
        request=request, template_name="blog/post/list.html", context={"posts": posts}
    )


def post_detail(request: HttpRequest, pk: int):
    post = get_object_or_404(klass=Post, id=pk, status=Post.Status.PUBLISH)
    return render(
        request=request, template_name="blog/post/detail.html", context={"post": post}
    )
