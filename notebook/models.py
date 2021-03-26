import os
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.urls import reverse
from PIL import Image
from slugify import slugify
import urllib
import datetime
from django.urls import reverse


# Create your models here.

# View program status
STATUS = (
    (0, "To watch"),
    (1, "Watching"),
    (2, "Watched"),
)

# Program formats type
FORMATS = (
    (0, "Movie"),
    (1, "Serie"),
    (2, "Documentary"),
    (3, "Comic book"),
    (4, "Book"),
    (5, "Game"),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(default="default-slug-profile", max_length=70)
    bio = models.TextField()
    pic = models.ImageField(
        default="profile_pics/default.png", upload_to="profile_pics"
    )

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return str(f"{self.user.username}'s Profile ")


    def get_absolute_url(self):
        return reverse("notebook:profile", kwargs={"pk": self.pk, "slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)
        img = Image.open(self.pic.path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.pic.path)


class Provider(models.Model):
    provider_name = models.CharField(max_length=70)
    slug = models.SlugField(default="default-slug-profile", max_length=80)
    provider_tmdb_id = models.IntegerField(blank=True, null=True, unique=True)
    provider_type = models.CharField(max_length=10, null=True)
    logo_url = models.CharField(max_length=100, null=True)
    logo_path = models.ImageField(
        default="program_posters/poster_default.png",
        upload_to="providers_posters",
        null=True,
    )

    class Meta:
        ordering = ["provider_name"]

    def __str__(self):
        return str(f"{self.provider_name}")

    def get_absolute_url(self):
        return reverse("notebook:provider", kwargs={"pk": self.pk})

    def get_remote_image(self):
        if self.logo_url and self.logo_path == "program_posters/poster_default.png":
            result = urllib.request.urlretrieve(
                f"https://www.themoviedb.org/t/p/original{self.logo_url}"
            )
            self.logo_path.save(
                os.path.basename(self.logo_url), File(open(result[0], "rb"))
            )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.provider_name)
        super().save(*args, **kwargs)
        img = Image.open(self.logo_path.path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.logo_path.path)
        self.get_remote_image()


class Program(models.Model):
    tmdb_id = models.IntegerField(blank=True, null=True, unique=True)
    name = models.CharField(max_length=70)
    original_name = models.CharField(max_length=70, null=True)
    slug = models.SlugField(max_length=70, default="default-slug-program")
    format = models.IntegerField(choices=FORMATS, default=0)
    tags = models.CharField(max_length=90, null=True)
    source = models.CharField(max_length=30, null=True)
    synopsis = models.TextField(null=True)
    homepage_link = models.CharField(max_length=200, null=True)
    watch_link = models.CharField(max_length=150, null=True)
    release_date = models.DateTimeField(null=True)
    last_air_date = models.DateTimeField(null=True)
    available_date = models.DateTimeField(null=True)
    origin_country = models.CharField(max_length=350, null=True)
    providers = models.ManyToManyField(Provider)
    poster_path = models.CharField(max_length=100, null=True)
    poster = models.ImageField(
        default="program_posters/poster_default.png",
        upload_to="program_posters",
        null=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse(
            "notebook:program-detail", kwargs={"slug": self.slug, "pk": self.pk}
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        img = Image.open(self.poster.path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.poster.path)


class ViewProgram(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile"
    )
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="program"
    )
    date = models.DateTimeField()
    chapter = models.CharField(max_length=10)
    comment = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.program.__str__

    def get_absolute_url(self):
        return reverse("notebook:viewprogram-detail", kwargs={"pk": self.pk})

    @property
    def get_html_url(self):
        url = reverse('notebook:viewprogram-edit', kwargs={"pk": self.pk})
        return f"<a href='{url}'>{self.program.name}</a>"
