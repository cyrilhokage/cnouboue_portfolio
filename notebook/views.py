from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.http import request
from django.contrib.auth.decorators import login_required
from .forms import UserRegistration, UserEditForm, Login_form, Watchs_Form, SignupForm, Program_Form
from .models import Watchs
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.template import loader
from django.views import generic
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Create your views here.

#The index view
def index(request):
    #if the user is authenticated
    if not request.user.is_authenticated :
        
        try:
            watched_list = Watchs.objects.filter(user=request.user.id)
        except Watchs.DoesNotExist:
            raise Http404("Watchs or User does not exist")
            
        template = 'notebook/userIndex.html'
        context = {'watched_list' : watched_list}
        
    else:
        
        form = Login_form()
        
        template = 'registration/login.html'
        
        context = {'form':form}
    
    return render(request, template, context)
    #return HttpResponse('Please Log in with valid credentials')


#Sing Up View
def signup(request):

	template="registration/signup.html"
	activation_mail_template = "registration/acc_active_email.html"


	if request.method == 'POST':

		form = SignupForm(request.POST)

		if form.is_valid():

			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your blog account.'
			message = render_to_string( activation_mail_template, {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token':account_activation_token.make_token(user),
            })

			to_email = form.cleaned_data.get('email')
			email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )

			email.send()

			return HttpResponse('Please confirm your email address to complete the registration')

	else:
		form = SignupForm()


	context = {'form': form}

	return render(request, template, context)

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
		
		return redirect('notebook:user_view', user.id )
		
	else:
		return HttpResponse('Activation link is invalid!')


"""
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'notebook/edit.html', context=context)
"""

#The user view
def user_view(request, user_id):
    #if the user is authenticated
    if request.user.is_authenticated :
        
        try:
            watched_list = Watchs.objects.filter(user=request.user.id)
        except Watchs.DoesNotExist:
            raise Http404("Watchs or User does not exist")
            
        template = 'notebook/userIndex.html'
        context = {'watched_list' : watched_list}
        
    else:
        
        form = Login_form()
        
        template = 'registration/login.html'
        
        context = {'form':form}
        
    
    return render(request, template, context)


#The watch view
def watch_view(request, watch_id):
    response = "Vous etes sur la page d'une watch dont l'id est : %s ."
    
    """
    try:
        track_list = Track.objects.filter(playlist=playlist_id)
    except Playlist.DoesNotExist:
        raise Http404("Playlist Does not exist")
    """
    
    template = 'notebook/watch.html'
    # context = {'track_list' : track_list}
    
    # return render(request, template, context)
    return render(request, template)


#The program view
def program_view(request, program_id):
    response = "Vous etes sur la page d'une watch dont l'id est : %s ."
    
    """
    try:
        track_list = Track.objects.filter(playlist=playlist_id)
    except Playlist.DoesNotExist:
        raise Http404("Playlist Does not exist")
    """
    
    template = 'notebook/program.html'
    # context = {'track_list' : track_list}
    
    # return render(request, template, context)
    return render(request, template)


# Add program view
def add_program_view(request):

	template="notebook/program_edit.html"

	if request.method == 'POST':

		form = Program_Form(request.POST)

		if form.is_valid():

			program = form.save(commit=False)
			program.save()

			return redirect('notebook:program', program.id )

	else:
		form = Program_Form()


	context = {'form':form}

	return render(request, template, context)


# Add watch view
def add_watch_view(request):

	template="notebook/watch_edit.html"

	if request.method == 'POST':

		form = Watchs_Form(request.POST)

		if form.is_valid():

			watch = form.save(commit=False)
			user = request.user 
			watch.user = user 

			watch.save()

			return redirect('notebook:watch', watch.id )

	else:
		form = Watchs_Form()


	context = {'form':form}

	return render(request, template, context)

