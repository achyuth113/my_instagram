from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import profile
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class SignupForm(forms.Form):
    first_name=forms.CharField(label="full_name",required=True,widget=forms.TextInput)
    email=forms.EmailField(label="email",required=True,widget=forms.EmailInput)
    username = forms.CharField(label="username",required=True,widget=forms.TextInput)
    password = forms.CharField(label="password",required=True,widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(label="username",required=True,widget=forms.TextInput)
    password = forms.CharField(label="password",required=True,widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    use_required_attribute = False
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'id': 'customImage'}))
    class Meta:
        model = profile
        exclude = ['id','user_id']

class UserForm2(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
