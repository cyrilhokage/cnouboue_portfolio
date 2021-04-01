from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    UserUpdateForm,
    ProfileUpdateForm,
    ProgramUpdateForm,
    UserRegistrationForm,
)
from django import forms
from django.core.paginator import Paginator
import calendar
from django.db import IntegrityError

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
from django.urls import reverse_lazy
from django.utils.html import mark_safe, format_html

# CRUD views
from .models import Program, Profile, ViewProgram
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .utils import Calendar

# For search
import requests
import json
from datetime import datetime, timedelta, date
from .notebookfunctions import getProgramData, getProviders


# Create your views here.


def index(request):
    return render(request, "notebook/index.html")


class HomeView(ListView):
    model = Program
    context_object_name = "programs"
    template_name = "notebook/index.html"
    ordering = ["-release_date"]


#######            Profile Views    ###################


def profileListView(request):
    listProfiles = Profile.objects.all()
    context = {"listProfiles": listProfiles}
    template = "notebook/profiles_list.html"
    return render(request, template, context)


class profileDetailsView(ListView):
    model = ViewProgram
    template_name = "notebook/profile_detail.html"

    # template_name = 'notebook/calendar.html'
    # success_url = reverse_lazy("notebook:calendar")

    def get_date(self, req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split("-"))
            return date(year, month, day=1)
        return datetime.today()

    def prev_month(self, d):
        first = d.replace(day=1)
        prev_month = first - timedelta(days=1)
        month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
        return month

    def next_month(self, d):
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        last = d.replace(day=days_in_month)
        next_month = last + timedelta(days=1)
        month = "month=" + str(next_month.year) + "-" + str(next_month.month)
        return month

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = self.get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month, self.kwargs["pk"])
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = self.prev_month(d)
        context["next_month"] = self.next_month(d)

        profile_user = get_object_or_404(User, id=self.kwargs["pk"])
        context["profile_user"] = profile_user

        context["watchlist"] = ViewProgram.objects.filter(
            profile=profile_user.profile, status=0
        )
        context["in_progress"] = ViewProgram.objects.filter(
            profile=profile_user.profile, status=1
        )
        context["completed"] = ViewProgram.objects.filter(
            profile=profile_user.profile, status=2
        )

        return context

    # return render(request, template, context)


# @login_required
# def profileUserView(request):
class profileUserView(LoginRequiredMixin, ListView):

    model = ViewProgram
    template_name = "notebook/profile_user.html"

    # template_name = 'notebook/calendar.html'
    # success_url = reverse_lazy("notebook:calendar")

    def get_date(self, req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split("-"))
            return date(year, month, day=1)
        return datetime.today()

    def prev_month(self, d):
        first = d.replace(day=1)
        prev_month = first - timedelta(days=1)
        month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
        return month

    def next_month(self, d):
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        last = d.replace(day=days_in_month)
        next_month = last + timedelta(days=1)
        month = "month=" + str(next_month.year) + "-" + str(next_month.month)
        return month

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = self.get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month, self.request.user.id)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = self.prev_month(d)
        context["next_month"] = self.next_month(d)

        context["watchlist"] = ViewProgram.objects.filter(
            profile=self.request.user.profile, status=0
        )
        context["in_progress"] = ViewProgram.objects.filter(
            profile=self.request.user.profile, status=1
        )
        context["completed"] = ViewProgram.objects.filter(
            profile=self.request.user.profile, status=2
        )

        return context

    # return render(request, template, context)


class CalendarView(ListView):
    model = ViewProgram
    template_name = "notebook/calendar.html"
    # success_url = reverse_lazy("notebook:calendar")

    def get_date(self, req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split("-"))
            return date(year, month, day=1)
        return datetime.today()

    def prev_month(self, d):
        first = d.replace(day=1)
        prev_month = first - timedelta(days=1)
        month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
        return month

    def next_month(self, d):
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        last = d.replace(day=days_in_month)
        next_month = last + timedelta(days=1)
        month = "month=" + str(next_month.year) + "-" + str(next_month.month)
        return month

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = self.get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        # context['calendar'] = format_html(mark_safe("<div><h1> Hello </h1></div>"))
        context["calendar"] = html_cal
        context["prev_month"] = self.prev_month(d)
        context["next_month"] = self.next_month(d)

        return context


@login_required
def profileUpdateView(request, pk):

    if request.method == "POST":
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            # messages.success(request,'Your Profile has been updated!')
            return redirect(
                "notebook:profile", request.user.id, request.user.profile.slug
            )

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {"p_form": p_form, "u_form": u_form}
    return render(request, "notebook/profile_update.html", context)


# Register and Activate account views
def register(request):

    template = "registration/register.html"
    activation_mail_template = "registration/activation_mail_temp.html"

    if request.method == "POST":  # if the form has been submitted
        form = UserRegistrationForm(request.POST)  # form bound with post data

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            to_email = form.cleaned_data.get("email")
            mail_subject = "Activate your Notebook account."
            message = render_to_string(
                activation_mail_template,
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )

            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            # return redirect('notebook:profile')
            return HttpResponse(
                "Please confirm your email address to complete the registration"
            )

    else:
        form = UserRegistrationForm()
    return render(request, template, {"form": form})


# Activation view
def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        return redirect("notebook:profile-user")

    else:
        # messages.error(request, "Oh oh ! Activation link is invalid :( ! ")
        return HttpResponse("Activation link is invalid!")


##########        CRUD views for programs      #######################


class ProgramDetailView(DetailView):
    model = Program
    template_name = "notebook/program_detail.html"
    context_object_name = "program"


class ProgramCreateView(LoginRequiredMixin, CreateView):
    model = Program
    fields = ["name", "format", "synopsis"]
    # fields = ['name', 'format', 'tags', 'source', 'release_date', 'available_date', 'poster']


def ProgramNew(request, media_type, tmdb_id):

    list_providers, link = getProviders(tmdb_id=tmdb_id, media_type=media_type)
    program = getProgramData(tmdb_id=tmdb_id, media_type=media_type)

    try:
        if program is not False:
            program["watch_link"] = link
            new_program = Program(**program)
            new_program.save()

            if list_providers is not False:
                for provider in list_providers:
                    new_program.providers.add(provider)

            return redirect("notebook:program-detail", new_program.slug, new_program.pk)

        else:
            return redirect("notebook:index")

    except IntegrityError:
        e_program = get_object_or_404(Program, tmdb_id=program["tmdb_id"])
        return redirect("notebook:program-detail", e_program.slug, e_program.pk)


def programListView(request):
    programs = Program.objects.all()

    paginator = Paginator(programs, 5)  # Show 25 contacts per page
    page = request.GET.get("page")

    try:
        listPrograms = paginator.get_page(page)
    except PageNotAnInteger:
        listPrograms = paginator.get_page(1)
    except EmptyPage:
        listPrograms = paginator.get_page(paginator.num_pages)

    context = {"listPrograms": listPrograms}
    template = "notebook/programs_list.html"

    return render(request, template, context)


@login_required
def ProgramUpdateView(request, pk):

    program = get_object_or_404(Program, id=pk)

    if request.method == "POST":
        form = ProgramUpdateForm(request.POST or None, request.FILES, instance=program)

        if form.is_valid():
            form.save()
            # messages.success(request,'The program has been updated!')
            return redirect("notebook:program-detail", program.slug, program.pk)

    else:
        form = ProgramUpdateForm(instance=program)

    template = "notebook/program_update.html"
    context = {"form": form, "program": program}

    return render(request, template, context)


class programDeleteView(LoginRequiredMixin, DeleteView):
    model = Program
    success_url = "/notebook/programs/"

    def get_test_func(self):
        model = self.get_object()
        return True


###### View programs CRUD #######


class ViewProgramDetailView(DetailView):
    model = ViewProgram
    template_name = "notebook/view_program_detail.html"
    context_object_name = "view"


class ViewProgramCreateView(LoginRequiredMixin, CreateView):

    model = ViewProgram
    fields = ["program", "status", "date", "chapter", "comment"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date"].widget = forms.DateInput(
            format=("%m/%d/%Y"),
            attrs={
                "class": "form-control",
                "placeholder": "Select a date",
                "type": "date",
            },
        )
        return form

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


class ViewProgramUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ViewProgram
    fields = ["program", "status", "date", "chapter", "comment"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date"].widget = forms.DateInput(
            format=("%m/%d/%Y"),
            attrs={
                "class": "form-control",
                "placeholder": "Select a date",
                "type": "date",
            },
        )
        return form

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        view = self.get_object()
        return self.request.user == view.profile.user


class ViewProgramDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Program
    success_url = "/notebook/programs/"

    def get_test_func(self):
        view = self.get_object()
        return self.request.user == view.profile.user


### Search program View


def ViewSearch(request):
    template = "notebook/index.html"

    if request.method == "GET":
        query = request.GET.get("q")

        submitbutton = request.GET.get("submit")

        if query is not None:
            # lookups= Q(title__icontains=query) | Q(content__icontains=query)
            params = dict(
                api_key="69cce8dbf435199baf4ab9dfcb63616d",
                include_adult="false",
                language="fr-FR",
                query=query,
            )

            try:
                req = requests.get("https://api.themoviedb.org/3/search/multi", params)
                if req.status_code == 200:
                    results = json.loads(req.content)
                else:
                    results = dict(results=[])

            except KeyError:
                pass

            context = {"results": results["results"], "submitbutton": submitbutton}

            return render(request, template, context)

        else:
            return render(request, template)

    else:
        return render(request, template)


# View for program's similars programs
def ProgramSimilarsView(request, pk, slug):

    template = "notebook/programSimilars.html"
    program = get_object_or_404(Program, id=pk)
    media_type = "tv" if program.format == 1 else "movie"

    try:
        params = dict(
            api_key="69cce8dbf435199baf4ab9dfcb63616d", language="fr-FR", page=1
        )
        req_reco = requests.get(
            f"https://api.themoviedb.org/3/{media_type}/{program.tmdb_id}/recommendations",
            params,
        )
        if req_reco.status_code == 200:
            data_reco = json.loads(req_reco.content)
        else:
            # print(f"Status code : {req_reco.status_code}")
            raise KeyError
    except KeyError:
        pass

    context = {"similarsPrograms": data_reco["results"][:5], "media_type": media_type}

    return render(request, template, context)
