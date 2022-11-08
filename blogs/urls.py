from django.urls import path

from blogs.views import PostListView, post_detail, post_share

app_name = "blogs"
urlpatterns = [
    # path("", post_list, name="post_list"),
    path("", PostListView.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>", post_detail, name="post_details"
    ),
    path("<int:post_id>/share", post_share, name="post_share")
]
