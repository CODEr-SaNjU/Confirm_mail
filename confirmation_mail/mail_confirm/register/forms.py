from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
class SignUpForm(UserCreationForm):
    email=forms.EmailField(max_length=30, required=True)
    username = forms.CharField( max_length=20, required=True)
    

    class Meta(ModelForm):
        model= User
        fields=['username','email','password1','password2',]