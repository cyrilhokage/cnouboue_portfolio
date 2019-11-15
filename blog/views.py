from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from .models import Post


# Create your views here.

"""
class PostList(generic.ListView):


	latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
    
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'

  """
"""
class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    """


def index(request):

	post_list =  Post.objects.order_by('-created_on')[:5]
	context = {'post_list':post_list}
	return render(request, 'blog/index.html', context)

def post(request, slug):
	post = Post.objects.get(slug=slug)
	context = {'post':post}
	return render(request, 'blog/article_detail.html', context)