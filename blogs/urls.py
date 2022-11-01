from django.urls import path

from blogs.views import post_detail, post_list

app_name = "blogs"
urlpatterns = [
    path("", post_list, name="post_list"),
    path("<int:pk>", post_detail, name="post_details"),
]
