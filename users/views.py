from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blog import models as blog_models
from django.contrib import messages
from .models import Profile, Follow, Notification
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Account successfully created for { username }! You can Login now.')
                return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
    
@login_required   
def profile(request):
    user_profile = request.user
    followers = Follow.objects.filter(followed=user_profile).select_related('follower')
    following = Follow.objects.filter(follower=user_profile).select_related('followed')
    followers_count = Follow.objects.filter(followed=user_profile).count()
    following_count = Follow.objects.filter(follower=user_profile).count()
    post_count = blog_models.Post.objects.filter(author=user_profile).count()
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile updated!')
            return redirect('my_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_profile': user_profile,
        'followers': followers,
        'following': following,
        'followers_count': followers_count,
        'following_count': following_count,
        'post_count': post_count
    }
    return render(request, 'users/my-profile.html', context)

def user_profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    followers_count = Follow.objects.filter(followed=user_profile).count()
    following_count = Follow.objects.filter(follower=user_profile).count()
    post_count = blog_models.Post.objects.filter(author=user_profile).count()
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, followed=user_profile).exists()

    context = {
        'user_profile': user_profile,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'post_count': post_count,
    }
    return render(request, 'users/profile.html', context)


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    user = request.user
    if user_to_follow != request.user:
        follow, created = Follow.objects.get_or_create(follower=user, followed=user_to_follow)
        if created:
            if not Notification.objects.filter(recipient=user_to_follow, sender=user, notification_type='follow').exists():
                Notification.objects.create(
                    recipient=user_to_follow,
                    sender=user,
                    notification_type='follow',
                )
            return JsonResponse({'status': 'followed'})
        else:
            follow.delete()
            return JsonResponse({'status': 'unfollowed'})
    return JsonResponse({'status': 'error'})


def followers_following(request, username):
    # Get the user whose profile is being viewed
    user_profile = get_object_or_404(User, username=username)
    
    # Get followers and following lists
    followers = Follow.objects.filter(followed=user_profile).select_related('follower')
    following = Follow.objects.filter(follower=user_profile).select_related('followed')
    
    context = {
        'user_profile': user_profile,
        'followers': followers,
        'following': following,
        'tab': request.GET.get('tab', 'followers'),  # Default to 'followers' tab if no tab is specified
    }
    return render(request, 'users/followers_following.html', context)

@login_required
def notifications(request):
    notifications = request.user.notifications.all().order_by('-timestamp')
    context = {'notifications': notifications}
    return render(request, 'users/notifications.html', context)