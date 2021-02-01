from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post
from datetime import datetime

class Static_Sitemap(Sitemap):

    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['main_home', 'blog']

    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):

        try:
            return item.updated_on
        except:
            return datetime.now()