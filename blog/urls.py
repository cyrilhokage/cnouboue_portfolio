from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.index, name='home'),
    path('post/<slug:slug>/', views.post, name='detail'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    #path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]