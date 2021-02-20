from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from slugify import slugify


# Create your models here.

#View program status
STATUS = (
    (0,"To watch"),
    (1,"Watching"),
    (2,"Watched"),
)

#Program formats type
FORMATS = (
    (0,"Film"),
    (1,"Serie"),
    (2,"Documentary"),
    (3,"Comic book"),
    (4,"Book"),
)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    slug = models.SlugField( default='default-slug-profile', max_length=70)
    bio=models.TextField()
    pic=models.ImageField(default='profile_pics/default.png',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}\'s Profile '
    
    def get_absolute_url(self):
        return reverse('notebook:profile', kwargs={'pk':self.pk, 'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)
        img = Image.open(self.pic.path)
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.pic.path)


class Program(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=70,  default='default-slug-program')
    format = models.IntegerField(choices=FORMATS, default=0)
    tags = models.CharField(max_length=90, null=True)
    source = models.CharField(max_length=30, null=True)
    synopsis = models.TextField(null=True)
    release_date = models.DateTimeField(null=True)
    available_date = models.DateTimeField(null=True)
    poster = models.ImageField(default='program_posters/poster_default.png', 
                                upload_to='program_posters',
                                null=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('notebook:program-detail', kwargs={ 'slug':self.slug ,'pk':self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        img = Image.open(self.poster.path)
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.poster.path)


class View_program(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program')
    date = models.DateTimeField()
    chapter = models.CharField(max_length=10)
    comment = models.TextField()
    status =  models.IntegerField(choices=STATUS, default=0)
    
    def __str__(self):
        return self.program.__str__
