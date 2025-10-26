from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpRequest, HttpResponse
from django.core.paginator import Paginator

from blog.models import Post


# Create your views here.


def post_list(request: HttpRequest) -> HttpResponse:
    post_list = Post.published.all()
    paginator = Paginator(object_list=post_list, per_page=3)
    page_number = request.GET.get("page", default=1)
    posts = paginator.get_page(number=page_number)
    return render(
        request=request, template_name="blog/post/list.html", context={"posts": posts}
    )


def post_detail(
    request: HttpRequest, year: int, month: int, day: int, post: str
) -> HttpResponse:
    post = get_object_or_404(
        klass=Post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
        status=Post.Status.PUBLISHED,
    )
    return render(
        request=request,
        template_name="blog/post/detail.html",
        context={"post": post},
    )
