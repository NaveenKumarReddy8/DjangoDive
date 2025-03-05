from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http.request import HttpRequest

from blog.models import Post

# Create your views here.


def post_list(request: HttpRequest):
    posts = get_list_or_404(klass=Post, status=Post.Status.PUBLISHED)
    return render(request=request, template_name="blog/post/list.html", context={"posts": posts})

def post_detail(request: HttpRequest, id: int):
    post = get_object_or_404(klass=Post, id=id)
    return render(request=request, template_name="blog/post/detail.html", context={"post": post})
