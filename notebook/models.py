from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.



class UserRegistrationModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Program(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    tags = models.CharField(max_length=500)
    source = models.CharField(max_length=100)
    synopsis = models.TextField()
    availability = models.IntegerField(default=0)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self',  related_name="friendship")
    wacthlist = models.ManyToManyField(Program, related_name="toWatch")


class Watchs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now= True)
    episode = models.CharField(max_length=100)
    comment = models.TextField()