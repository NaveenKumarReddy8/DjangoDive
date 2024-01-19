from django.contrib.sitemaps import (
    Sitemap,
    _SupportsCount,
    _SupportsLen,
    _SupportsOrdered,
)

from blog.models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self) -> _SupportsLen | _SupportsCount | _SupportsOrdered:
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
