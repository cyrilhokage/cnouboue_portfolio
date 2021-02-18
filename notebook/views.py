from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'notebook/index.html')


def register(request):
    if request.method == 'POST': #if the form has been submitted
        form = UserRegistrationForm(request.POST) #form bound with post data
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('notebook:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'register/register.html', {'form': form})
    
#@login_required
def profile(request):
    return render(request, 'notebook/profile.html')