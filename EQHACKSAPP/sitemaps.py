from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blog.models import NewsArticle, Post


class NewsArticleSitemap(Sitemap):

    priority = 0.8
    def items(self):
        return NewsArticle.objects.filter(status=NewsArticle.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_on
    
class PostSitemap(Sitemap):

    priority = 0.8
    def items(self):
        return Post.objects.filter(status=Post.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_on