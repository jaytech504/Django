from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from .models import Post, Like
from django.db.models import Exists, OuterRef
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_likes = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            context['user_likes'] = user_likes
        return context
    

class UserListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_likes = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            context['user_likes'] = user_likes
        return context
        
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_liked'] = Like.objects.filter(user=self.request.user, post=self.object).exists()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    liked = False
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
    except Like.DoesNotExist:
        Like.objects.create(user=request.user, post=post)
        liked = True

    like_count = post.like_set.count()
    return JsonResponse({'liked': liked, 'like_count': like_count})


def about(request):
    return render(request, 'blog/about.html',{'title' : 'About Page'})
