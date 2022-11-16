"""View layer for blogs."""

from typing import Optional

from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from blogs.forms import CommentForm, EmailPostForm
from blogs.models import Post

# Create your views here.


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request=request,
        template_name="blogs/post/comment.xhtml",
        context={"post": post, "form": form, "comment": comment},
    )


class PostListView(ListView):
    model = Post
    template_name = "blogs/post/list.xhtml"
    context_object_name: Optional[str] = "posts"
    paginate_by: int = 3


def post_list(request: HttpRequest, tag_slug=None):
    post_list = get_list_or_404(Post)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get("page", default=1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request=request, template_name="blogs/post/list.xhtml", context={"posts": posts, "tag": tag}
    )


def post_detail(request: HttpRequest, year: int, month: int, day: int, post: str):
    post = get_object_or_404(
        Post, publish__year=year, publish__month=month, publish__day=day, slug=post
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request=request,
        template_name="blogs/post/detail.xhtml",
        context={"post": post, "comments": comments, "form": form},
    )


def post_share(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    sent: bool = False
    if request.method == "POST":
        form: EmailPostForm = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned_data: dict = form.cleaned_data
            post_url: str = request.build_absolute_uri(post.get_absolute_url())
            subject: str = f"{cleaned_data['name']} recommends you read {post.title}"
            message: str = f"Read {post.title} at {post_url}\n\n{cleaned_data['name']}'s comments: {cleaned_data['comments']}"
            send_mail(
                subject=subject,
                message=message,
                from_email="mr.naveen8@gmail.com",
                recipient_list=[cleaned_data["to"]],
                fail_silently=False,
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request=request,
        template_name="blogs/post/share.xhtml",
        context={"post": post, "form": form, "sent": sent},
    )
