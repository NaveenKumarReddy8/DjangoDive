from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from markdown import markdown

from blogs.models import Post


class LatestPostsFeed(Feed):
    title = "Blogs"
    link = reverse_lazy("blogs:post_list")
    description = "New posts of my blog"

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item) -> str:
        return truncatewords_html(markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
