from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from blog.models import Post

# Create your views here.


def post_list(request: HttpRequest):
    post_list = Post.published.all()
    paginator = Paginator(object_list=post_list, per_page=3)
    page_number = request.GET.get("page", default=1)
    posts = paginator.page(page_number)
    return render(
        request=request, template_name="blog/post/list.html", context={"posts": posts}
    )


def post_detail(request: HttpRequest, year: int, month: int, day: int, post: str):
    post = get_object_or_404(
        klass=Post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
        status=Post.Status.PUBLISH,
    )
    return render(
        request=request, template_name="blog/post/detail.html", context={"post": post}
    )
