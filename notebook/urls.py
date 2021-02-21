from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'notebook'

urlpatterns = [

    # App index page
    path('', views.HomeView.as_view(), name='index'),

    ### Authentication urls

    # Signup / register and confirmation
    path('register/', views.register, name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),

    # Login
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    #Log out
    path('logout/', auth_views.LogoutView.as_view(template_name="registration/logout.html"), name='logout'),
    
    #Profile
    path('profile/', views.profileUserView, name='profile-user'),
    path("profiles/", views.profileListView, name="profile-list"),
    path('profiles/<int:pk>/<str:slug>', views.profileDetailsView, name='profile'), # actual user profile page
    path('profiles/edit/<int:pk>', views.profileUpdateView, name='profile-edit'), # edit user page
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

    ### CRUD urls for programs
    path("programs/", views.programListView, name="program-list"),
    path("programs/<str:slug>/<int:pk>", views.ProgramDetailView.as_view(), name="program-detail"),
    path("programs/create/new", views.ProgramCreateView.as_view(), name='program-create'),
    path("programs/<int:pk>/edit", views.ProgramUpdateView, name='program-edit'),
    path("programs/delete/<int:pk>/", views.programDeleteView.as_view(), name='program-delete'),

    ### CRUD urls for views
    path("view/<int:pk>", views.ViewProgramDetailView.as_view(), name="viewprogram-detail"),
    path("view/create/new",views.ViewProgramCreateView.as_view(),name='create'),
    path("view/edit/<int:pk>",views.ViewProgramUpdateView.as_view(),name='viewprogram-edit'),
    path("view/delete/<int:pk>/", views.ViewProgramDeleteView.as_view(), name='viewprogram-delete'),

]