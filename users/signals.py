from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from allauth.account.signals import user_signed_up

@receiver(user_signed_up)
def populate_profile_from_google(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        # Extract Google user data
        google_data = sociallogin.account.extra_data
        username = google_data.get('name')  # Google's name field
        email = google_data.get('email')
        
        # Update the user's profile fields
        user.username = username if username else user.username
        user.email = email if email else user.email
        user.save()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()