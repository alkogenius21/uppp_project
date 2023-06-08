from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import LibraryUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = LibraryUser
        fields = ('username', 'password1', 'password2', 'first_name', 'second_name', 'last_name', 'date_of_birth', 'email', 'phone')

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(label='Username')

