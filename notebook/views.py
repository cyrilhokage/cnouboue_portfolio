from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm

from django.contrib.auth import login, authenticate
from django.views import generic
from django.http import HttpResponse, Http404
from django.template import loader
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# Create your views here.

def index(request):
    return render(request, 'notebook/index.html')


# Login View
@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        u_form = UserUpdateForm(request.POST,instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your Profile has been updated!')
            return redirect('notebook:profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user)
        u_form = UserUpdateForm(instance=request.user.profile)

    context={'p_form': p_form, 'u_form': u_form}
    return render(request, 'notebook/profile.html',context )


# Register and Activate account views
def register(request):
    
    template = "registration/register.html"
    activation_mail_template = "registration/activation_mail_temp.html"
    
    if request.method == 'POST': #if the form has been submitted
        form = UserRegistrationForm(request.POST) #form bound with post data

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            
            username = form.cleaned_data.get('username')
            messages.success(request, "Please confirm your email address to validate {{username}}'s account")

            current_site = get_current_site(request)
            to_email = form.cleaned_data.get('email')
            mail_subject = "Activate your Notebook account."
            message = render_to_string( activation_mail_template, {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })

            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            user.save()

            username = form.cleaned_data.get('username')
            messages.success(request, "Please confirm your email address to validate {{username}}'s account")

            # return redirect('notebook:profile')
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = UserRegistrationForm()
    return render(request, template, {'form': form})


# Activation view
def activate(request, uidb64, token):
    
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        
        return redirect('notebook:profile')
		
    else:
        messages.error(request, "Oh oh ! Activation link is invalid :( ! ")
        return HttpResponse('Activation link is invalid!')
