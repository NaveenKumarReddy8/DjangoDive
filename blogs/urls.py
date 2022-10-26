from django.urls import path

from blogs.views import post_detail, post_list

urlpatterns = [
    path("", post_list, name="postlist"),
    path("post_details/<int:pkid>", post_detail, name="postdetails"),
]
