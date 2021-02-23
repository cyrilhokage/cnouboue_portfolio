"""cnouboue_portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings  # new
from django.conf.urls.static import static  # new
from blog import views
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from blog.models import Post
from blog.sitemaps import Static_Sitemap

info_dict = {
    "queryset": Post.objects.filter(status=1),
    "date_field": "updated_on",
}

sitemaps = {
    "static": Static_Sitemap,
    "blog": GenericSitemap(info_dict, priority=0.6),
}


urlpatterns = [
    path("", views.home, name="main_home"),
    path("", include("django.contrib.auth.urls")),  # Authentication urls
    path("admin/", admin.site.urls),  # Admin urls
    path("blog/", include("blog.urls"), name="blog"),
    path("notebook/", include("notebook.urls")),
    # the sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
