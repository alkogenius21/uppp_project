# -*- coding: cp1251 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import LibraryUser, Book, News_paper

class RegistrationForm(UserCreationForm):
    class Meta:
        model = LibraryUser
        fields = ('username', 'password1', 'password2', 'first_name', 'second_name', 'last_name', 'date_of_birth', 'email', 'phone')

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class NewsForm(forms.ModelForm):
    class Meta:
        model = News_paper
        fields = '__all__'

class EditProfileForm(forms.Form):
    class Meta:
        model = LibraryUser
        fields = ('username', 'first_name', 'second_name', 'last_name', 'date_of_birth', 'email', 'phone')

class ProblemReportForm(forms.Form):
    problem_title = forms.CharField(label='�������� ��������', max_length=100)
    problem_description = forms.CharField(label='�������� ��������', widget=forms.Textarea)
    problem_photo = forms.ImageField(label='���� ��������', required=False)