from dataclasses import field

from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from .models import * 

class UserForm(UserCreationForm):
	

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(UserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class UpdateUserForm(UserChangeForm):
    password=None

    class Meta:
        model = User
        fields = ("username", "email")



class ChangeUserPassword(PasswordChangeForm):
	name=None
	email=None

	class Meta:
		model = User
		fields = ( "password1", "password2")


class ResetPass(UserCreationForm):
	username=None

	class Meta:
		model = User
		fields = ( "password1", "password2")

