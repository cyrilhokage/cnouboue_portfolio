from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'notebook'

urlpatterns = [

    # App index page
    path('', views.index, name='index'),

    ### Authentication urls

    # Signup / register and confirmation
    path('register/', views.register, name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),

    # Login
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    #Log out
    path('logout/', auth_views.LogoutView.as_view(template_name="registration/logout.html"), name='logout'),
    
    #Profile
    path('profile/', views.profile, name='profile'), # actual user profile page
    #path('profile/<str:uidb64>/', views.profile, name='profile'),  #User profile page
    
    # Password reset urls
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name = 'registration/password_reset_email.html'),
        name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
    name='password_reset_confirm'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),
    path('password-reset-complete/',
auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),

]