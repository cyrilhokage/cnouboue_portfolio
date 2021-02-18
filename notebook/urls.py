from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'notebook'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='register/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="register/logout.html"), name='logout'),
    path('profile/', views.profile, name='profile'),
]