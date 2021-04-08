from django.db import models
from django.contrib.auth.models import User
from django.contrib.sitemaps import ping_google

# Create your models here.
STATUS = ((0, "Draft"), (1, "Published"))

CONTEXT = ((0, "Private"), (1, "School"), (2, "Pro"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    html_content = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    main_image = models.ImageField(upload_to="images/", blank=True)
    github_link = models.CharField(
        max_length=500, default="https://github.com/cyrilhokage"
    )
    context = models.IntegerField(choices=CONTEXT, default=0)
    technos = models.CharField(max_length=500)
    summary = models.CharField(max_length=500)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/" + self.slug

    # Overwrite save() method to send new sitemap to google when a post is updated
    def save(self,  *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            ping_google()
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
