from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Post

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Enter the title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter the content'}))
    

    class Meta:
        model = Post
        fields = ['title', 'content'] 