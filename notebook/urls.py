from django.urls import path
from . import views as views
from django.urls import reverse_lazy
from django.contrib.auth import views as Views

app_name = 'notebook'

urlpatterns = [

    path('', views.index, name='index'),

    ####	Authentification URLS

    #To login
	path('login/', Views.LoginView.as_view(template_name='registration/login.html'), name='login'),  #ex: /Music/login/

    #To logout
	path('logout/', Views.LogoutView.as_view(), name='logout'),  #ex: /Music/logout/

    #To reset password
	path('password-reset/', Views.PasswordResetView.as_view(), name='password_reset'),
	path('password-reset/done/', Views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', Views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),	
	path('reset/done/', Views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #To change passwords
	path('password-change/', Views.PasswordChangeView.as_view(), name='password_change'),
	path('password-change/done/', Views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    #to handle sign up with confirmation
	path('signup/', views.signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),


    ####	Other URLS

    #User index
	path('user/<int:user_id>/', views.user_view, name="user_view"),	#ex: /Music/5
     
    #To display watch
	path('watch/<int:watch_id>/', views.watch_view, name='watch'),
    path('watch/add/', views.add_watch_view, name='watch_add'),

    #To display program
	path('program/<int:program_id>/', views.program_view, name='program'),
    path('program/add/', views.add_program_view, name='program_add'),

]