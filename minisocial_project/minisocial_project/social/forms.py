from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("body",)
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "What's happening?"})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {"body": forms.TextInput(attrs={"placeholder": "Write a comment…", "maxlength": 500})}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "avatar_url")
        widgets = {"bio": forms.Textarea(attrs={"rows": 3, "placeholder": "A little about you"}), "avatar_url": forms.URLInput(attrs={"placeholder": "https://example.com/avatar.jpg"})}
