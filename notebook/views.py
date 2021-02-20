from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, ProgramUpdateForm

# Authentication & validation imports
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

# CRUD views
from .models import Program, Profile
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def index(request):
    return render(request, 'notebook/index.html')

class HomeView(ListView):
    model = Program
    context_object_name = 'programs'
    template_name = 'notebook/index.html'
    ordering = ['-release_date']


#######            Profile Views    ###################

def profileListView(request):
    listProfiles = Profile.objects.all()
    context = {'listProfiles':listProfiles}
    template = 'notebook/profiles_list.html'
    return render(request, template, context)


def profileDetailsView(request, pk, slug):
    template = 'notebook/profile_detail.html'
    profile_user = get_object_or_404(User, id=pk)
    context = {'profile_user': profile_user}
    return render(request, template, context)

@login_required
def profileUserView(request):
    template = 'notebook/profile_user.html'
    return render(request, template)


@login_required
def profileUpdateView(request, pk):

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            # messages.success(request,'Your Profile has been updated!')
            return redirect('notebook:profile', request.user.id, request.user.profile.slug)
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context={'p_form': p_form, 'u_form': u_form}
    return render(request, 'notebook/profile_update.html', context)


# Register and Activate account views
def register(request):
    
    template = "registration/register.html"
    activation_mail_template = "registration/activation_mail_temp.html"
    
    if request.method == 'POST': #if the form has been submitted
        form = UserRegistrationForm(request.POST) #form bound with post data

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # username = form.cleaned_data.get('username')
            # messages.success(request, "Please confirm your email address to validate {{username}}'s account")

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

            # username = form.cleaned_data.get('username')
            # messages.success(request, "Please confirm your email address to validate {{username}}'s account")

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
        
        return redirect('notebook:profile', user.pk)
		
    else:
        # messages.error(request, "Oh oh ! Activation link is invalid :( ! ")
        return HttpResponse('Activation link is invalid!')



########## CRUD views for programs              #############################
class ProgramDetailView(DetailView):
    model = Program  
    template_name='notebook/program_detail.html'
    context_object_name = 'program'

class ProgramCreateView(LoginRequiredMixin, CreateView):
    model = Program
    fields=['name', 'format', 'synopsis']
    # fields = ['name', 'format', 'tags', 'source', 'release_date', 'available_date', 'poster']


def programListView(request):
    listPrograms = Program.objects.all()
    context = {'listPrograms':listPrograms}
    template = 'notebook/programs_list.html'
    return render(request, template, context)

@login_required
def ProgramUpdateView(request, pk):

    program = get_object_or_404(Program, id=pk)

    if request.method == 'POST':
        form = ProgramUpdateForm(request.POST or None, request.FILES, instance=program)

        if form.is_valid():
            form.save()
            # messages.success(request,'The program has been updated!')
            return redirect('notebook:program-detail', program.slug, program.pk)
    
    else:
        form = ProgramUpdateForm(instance=program)

    template = "notebook/program_update.html"
    context = {'form': form, 'program': program}

    return render(request, template, context) 
        

def edit_program(request):
    return HttpResponse('<h1>Update your post..</h1>')

def delete_program(request):
    return HttpResponse('<h1>Delete a post..</h1>')
