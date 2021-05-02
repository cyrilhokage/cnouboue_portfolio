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
import requests
import json


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

API_KEY = os.environ.get("TMDB_TOKEN", "test")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(default="default-slug-profile", max_length=70)
    bio = models.TextField()
    following = models.ManyToManyField("self")
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
        default="providers_posters/default-provider.jpg",
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
        if self.logo_url and self.logo_path == "providers_posters/default-provider.jpg":
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
        if img.height > 700 or img.width > 700:
            output_size = (700, 700)
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
    similars = models.ManyToManyField("self")
    providers = models.ManyToManyField(Provider)
    poster_path = models.CharField(max_length=100, null=True)
    poster = models.ImageField(
        default="program_posters/default-poster.jpg",
        upload_to="program_posters",
        null=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name) if self.name else ""

    def get_absolute_url(self):
        return reverse(
            "notebook:program-detail", kwargs={"slug": self.slug, "pk": self.pk}
        )

    """
    Method to get programs similars programs
    """

    def addSimilarPrograms(self):

        media_type = "tv" if self.format == 1 else "movie"

        try:
            params = dict(
                api_key=API_KEY, language="fr-FR", page=1
            )
            req_reco = requests.get(
                f"https://api.themoviedb.org/3/{media_type}/{self.tmdb_id}/recommendations",
                params,
            )
            if req_reco.status_code == 200:
                data_reco = json.loads(req_reco.content)
            else:
                # print(f"Status code : {req_reco.status_code}")
                raise KeyError
        except KeyError:
            pass
        

        for program in data_reco["results"][:10]:
            similar_program_querry = Program.objects.filter(tmdb_id=program["id"])
            if (len(similar_program_querry)>0):
                for similar_program in similar_program_querry:
                    self.similars.add(similar_program)


    def get_remote_image(self):
        if self.poster_path and self.poster == "program_posters/default-poster.jpg":
            result = urllib.request.urlretrieve(
                f"https://www.themoviedb.org/t/p/original{self.poster_path}"
            )
            self.poster.save(
                os.path.basename(self.poster_path), File(open(result[0], "rb"))
            )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.addSimilarPrograms()
        super().save(*args, **kwargs)
        img = Image.open(self.poster.path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if img.height > 700 or img.width > 700:
            output_size = (700, 700)
            img.thumbnail(output_size)
            img.save(self.poster.path)
        self.get_remote_image()



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
        return str(
            f"{self.program.__str__()}'s view from {self.profile.user.username}  "
        )

    def get_absolute_url(self):
        return reverse("notebook:viewprogram-detail", kwargs={"pk": self.pk})

    @property
    def get_html_url(self):
        url = reverse("notebook:viewprogram-detail", kwargs={"pk": self.pk})
        return f"<a href='{url}'>{self.program.name}</a>"
