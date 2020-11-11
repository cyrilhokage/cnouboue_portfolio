from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

CONTEXT = (
	(0, "Private"),
	(1, "School"),
	(2, "Pro")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    main_image = models.ImageField(upload_to='images/', blank=True)
    github_link = models.CharField(max_length=500, default="https://github.com/cyrilhokage")
    context = models.IntegerField(choices=CONTEXT, default=0)
    technos = models.CharField(max_length=500)
    summary = models.CharField(max_length=500)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title