"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_view
from blog import views as blog_view
from chat import views as chat_view
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_view.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('blog.urls')), 
    path('user/<str:username>', blog_view.UserListView.as_view(), name = 'user-posts'),
    path('my-profile/', user_view.profile, name='my_profile'),
    path('profile/<str:username>/', user_view.user_profile, name='profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('follow/<str:username>/', user_view.follow_user, name='follow_user'),
    path('followers-following/<str:username>/', user_view.followers_following, name='followers_following'),
    path('notifications/', user_view.notifications, name='notifications'),
    path('chat/<int:user_id>/', chat_view.chat_view, name='chat'),
    path('chat/<int:conversation_id>/send_message/', chat_view.send_message, name='send_message'),
    path('chat/<int:conversation_id>/get_messages/', chat_view.get_messages, name='get_messages'),
    path('chats/', chat_view.chat_list_view, name='chat_list'),
    path('accounts/', include('allauth.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
