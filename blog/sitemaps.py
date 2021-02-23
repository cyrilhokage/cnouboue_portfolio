from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post
from datetime import datetime
from blog.urls import urlpatterns as blogUrls


class Static_Sitemap(Sitemap):

    priority = 0.6
    changefreq = "weekly"

    def items(self):
        urlList = ["main_home"]

        for url in blogUrls:
            if url.name != "detail":
                urlList.append("blog:" + url.name)
        return urlList

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):

        try:
            return item.updated_on
        except:
            return datetime.now()
