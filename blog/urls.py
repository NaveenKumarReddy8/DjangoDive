from django.urls import path

from blog.views import post_detail, post_list

url_patterns = [
    path("", post_list, name="post_list"),
    path("<int:id>/", post_detail, name="post_detail"),
]
