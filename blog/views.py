from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.decorators.http import require_POST

from blog.forms import EmailPostForm, CommentForm
from blog.models import Post

# Create your views here.


def post_list(request: HttpRequest):
    post_list = Post.published.all()
    paginator = Paginator(object_list=post_list, per_page=3)
    page_number = request.GET.get("page", default=1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request=request, template_name="blog/post/list.html", context={"posts": posts}
    )


class PostListView(ListView):
    model = Post
    paginate_by = 3
    context_object_name = "posts"
    template_name = "blog/post/list.html"


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


def post_share(request: HttpRequest, post_id: int):
    post = get_object_or_404(klass=Post, id=post_id, status=Post.Status.PUBLISH)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n {cd['name']}'s comments: {cd['comments']}"
            send_mail(
                subject=subject,
                message=message,
                from_email=cd["email"],
                recipient_list=(cd["to"],),
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request=request,
        template_name="blog/post/share.html",
        context={"post": post, "form": form, "sent": sent},
    )

@require_POST
def post_comment(request: HttpRequest, post_id: int):
    post = get_object_or_404(klass=Post, id=post_id, status=Post.Status.PUBLISH)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request=request, template_name="blog/post/comment.html", context={"form": form, "post": post, "comment": comment})