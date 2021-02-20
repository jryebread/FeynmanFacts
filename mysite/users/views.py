from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.paginator import Paginator
from blog.models import Post

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required #adds decorator that you must be logged in to access this template page
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated! :]')
            return redirect('profile') #causes browser to do get request
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    #THIS IS WRONG PAGINATION IS NOT SET UP CORRECTLY
    user_posts = Post.objects.filter(author=request.user).order_by('-date_posted')
    paginator = Paginator(user_posts, 15) # Show8 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
        'posts': user_posts,
        'page_obj': page_obj
    }
    return render(request, 'users/profile.html', context)
