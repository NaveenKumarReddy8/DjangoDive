from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http.request import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail


from blog.models import Post
from blog.forms import EmailPostForm

# Create your views here.


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request: HttpRequest):
    posts = get_list_or_404(klass=Post, status=Post.Status.PUBLISHED)
    page = Paginator(object_list=posts, per_page=3)
    page_number = request.GET.get("page", 1)
    try:
        posts = page.get_page(number=page_number)
    except EmptyPage:
        posts = page.get_page(number=page.num_pages)
    except PageNotAnInteger:
        posts = page.get_page(number=1)
    return render(request=request, template_name="blog/post/list.html", context={"posts": posts})


def post_detail(request: HttpRequest, year: int, month: int, day: int, post: str):
    post = get_object_or_404(klass=Post, publish__year=year, publish__month=month, publish__day=day, slug=post)
    return render(request=request, template_name="blog/post/detail.html", context={"post": post})


def post_share(request: HttpRequest, post_id: int):
    post = get_object_or_404(klass=Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject=subject, message=message, from_email=None, recipient_list=[cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request=request,
        template_name="blog/post/share.html",
        context={"post": post, "form": form, "sent": sent},
    )
