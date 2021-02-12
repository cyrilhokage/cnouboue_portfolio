from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Watchs, Program
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic
from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

# from .models import Profile



class UserRegistration(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

#Login Form
class Login_form(forms.Form):
	username = forms.CharField(max_length=100,
                                widget=forms.TextInput(attrs={'class':'input-1',
                                                                'placeholder':'username'}))
	password = forms.CharField(max_length=32,
                                widget=forms.PasswordInput(attrs={'class':'input-2',
                                                                    'placeholder':'password'}))


#Sign Up Form
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class Watchs_Form(forms.ModelForm):
	class Meta:
		model = Watchs
		exclude = ('id', 'user')

class Program_Form(forms.ModelForm):
    class Meta:
        model = Program
        exclude = ('id',)