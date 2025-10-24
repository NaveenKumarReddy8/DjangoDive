from django.shortcuts import render
from django.http import Http404, HttpRequest, HttpResponse

from blog.models import Post


# Create your views here.


def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.published.all()
    return render(
        request=request, template_name="blog/post/list.html", context={"posts": posts}
    )
