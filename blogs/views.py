"""View layer for blogs."""

from typing import Optional

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from blogs.forms import CommentForm, EmailPostForm, SearchForm
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
    post_list = Post.objects.all()
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
        request=request,
        template_name="blogs/post/list.xhtml",
        context={"posts": posts, "tag": tag},
    )


def post_detail(request: HttpRequest, year: int, month: int, day: int, post: str):
    post = get_object_or_404(
        Post, publish__year=year, publish__month=month, publish__day=day, slug=post
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_id = post.tags.values_list("id", flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    return render(
        request=request,
        template_name="blogs/post/detail.xhtml",
        context={
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
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


def post_search(request: HttpRequest):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector("title", weight="A") + SearchVector(
                "body", weight="B"
            )
            search_query = SearchQuery(query)
            results = (
                Post.objects.all()
                .annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                )
                .filter(rank__gte=0.1)
                .order_by("-rank")
            )
    return render(
        request=request,
        template_name="blogs/post/search.xhtml",
        context={"form": form, "query": query, "results": results},
    )
