"""Admin module for Django's Admin page."""

from django.contrib import admin

from blogs.models import Comment, Post

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin Model for the Post Model."""

    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin Model for the Comment Model."""

    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]
