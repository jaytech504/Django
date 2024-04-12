from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()
  
  class Meta:
  	model = User
  	fields = ['username', 'email', 'password1', 'password2']

class  UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		"""docstring for Meta"""
		model = User
		fields = ['username', 'email']

			
	"""docstring for  UserupdateForm"""
class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']
		"""docstring for Meta"""
		
			