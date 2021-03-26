from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Program, ViewProgram
from django.forms import ModelForm, DateInput


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    pic = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Profile
        fields = ["pic", "bio"]


class ProgramUpdateForm(forms.ModelForm):

    tags = forms.CharField(required=False)
    source = forms.CharField(required=False)
    release_date = forms.DateTimeField(required=False)
    available_date = forms.DateTimeField(required=False)
    poster = forms.ImageField(required=False)

    class Meta:
        model = Program
        fields = [
            "name",
            "format",
            "tags",
            "synopsis",
            "source",
            "release_date",
            "available_date",
            "poster",
        ]


class ProgramCreationForm(UserCreationForm):
    class Meta:
        model = Program
        # fields=['name', 'format', 'tags', 'source', 'release_date', 'available_date', 'poster']
        fields = ["name", "format", "synopsis"]


class SearchForm(forms.Form):
    class Meta:
        fields = ["search"]

