from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
)

from blog.models import Post
from blog.forms import EmailPostForm, CommentForm, SearchForm


# Create your views here.


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request: HttpRequest, tag_slug: None | str = None) -> HttpResponse:
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(klass=Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(object_list=post_list, per_page=3)
    page_number = request.GET.get("page", default=1)
    posts = paginator.get_page(number=page_number)
    return render(
        request=request,
        template_name="blog/post/list.html",
        context={"posts": posts, "tag": tag},
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
    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tag_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags",
        "-publish",
    )[:4]

    return render(
        request=request,
        template_name="blog/post/detail.html",
        context={
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
    )


def post_share(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(klass=Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            send_mail(
                subject=f"{cd['name']} recommends you read {post.title}",
                message=f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}",
                from_email=None,
                recipient_list=[cd["to"]],
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
def post_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(klass=Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request=request,
        template_name="blog/post/comment.html",
        context={"post": post, "form": form, "comment": comment},
    )


def post_search(request: HttpRequest) -> HttpResponse:
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = (
                Post.published.annotate(similarity=TrigramSimilarity("title", query))
                .filter(similarity__gt=0.1)
                .order_by("-similarity")
            )
    return render(
        request=request,
        template_name="blog/post/search.html",
        context={"form": form, "query": query, "results": results},
    )
