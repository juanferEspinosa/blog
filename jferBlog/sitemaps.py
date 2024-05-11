from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.conf import settings
from blog.models import Post



class StaticViewSitemap(Sitemap):
    priority = 0,5
    changefreq = "daily"

    def items(self):
        return ["homepage", "resume"]

    def location(self, item):
        return reverse(item)
    
class PostViewSitemap(Sitemap):
    priority = 0,5
    changefreq = "daily"

    def items(self):
        return Post.objects.all()