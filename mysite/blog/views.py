from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Like
from users.models import Profile
import json
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

@login_required
def send_like(request, pk):
    if request.method == 'POST': 
        post_id = request.POST.get('postid')
        print("postid: ", post_id)   
        post = get_object_or_404(Post, id=request.POST.get('postid'))    
        print("post ", post)
        user = request.user
        profile = Profile.objects.get(user=user)

        if user in post.liked.all():
            post.liked.remove(user)
        else:
            post.liked.add(user)
        
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)
        if not created:
            print(like.value)
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

        post.save()
        like.save()


        #we should update the posts like count here
        #only if we query the other likes table and see that they have not liked before
        data = {
            'value': like.value,
            'likes': post.liked.all().count()
        }
        return JsonResponse(data, safe=False)

    return redirect('blog-home')

class PostListSearchView(ListView):
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 7

    def get_queryset(self):
        query = self.request.GET.get('search')
        return Post.objects.filter(title__icontains=query)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context[''] = timezone.now()
    #     return context

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app> / <model>_<viewtype>.html # blog/post_detail.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app> / <model>_<viewtype>.html # blog/post_detail.html
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        #the form  you are trying to submit is the currently logged in user
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        #the form  you are trying to submit is the currently logged in user
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        #prevent others from editing another users posts
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        #prevent others from editing another users posts
        if self.request.user == post.author:
            return True
        else:
            return False
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})