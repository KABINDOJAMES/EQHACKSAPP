from django.contrib import admin
from django.urls import path, include
from EQHACKSAPP import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import NewsArticleSitemap, PostSitemap

sitemaps = {'newsarticle': NewsArticleSitemap, 'post': PostSitemap}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),

    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}),  
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.views.page_not_found"