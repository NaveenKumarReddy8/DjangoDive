from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISH)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISH = "PB", "Publish"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Model Managers.
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ("-publish",)
        indexes = (models.Index(fields=("-publish",)),)

    def __str__(self) -> str:
        return self.title