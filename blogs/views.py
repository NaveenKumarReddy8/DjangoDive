from typing import Optional

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView

from blogs.models import Post
from blogs.forms import EmailPostForm

# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = "blogs/post/list.xhtml"
    context_object_name: Optional[str] = "posts"
    paginate_by: int = 3


# This view function is replaced by class based View PostListView.
def post_list(request: HttpRequest):
    post_list = get_list_or_404(Post)
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get("page", default=1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request=request, template_name="blogs/post/list.xhtml", context={"posts": posts}
    )


def post_detail(request: HttpRequest, year: int, month: int, day: int, post: str):
    post = get_object_or_404(
        Post, publish__year=year, publish__month=month, publish__day=day, slug=post
    )
    return render(
        request=request, template_name="blogs/post/detail.xhtml", context={"post": post}
    )

def post_share(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form: EmailPostForm = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
    else:
        form = EmailPostForm()
    return render(request=request, template_name="blogs/post/share.xhtml", context={"post": post, "form": form})
