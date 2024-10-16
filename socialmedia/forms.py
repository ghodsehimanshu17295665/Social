from django import forms
<<<<<<< HEAD
from socialmedia.models import Post
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.models import User
from .models import User
=======
# from socialmedia.models import Post
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.models import User
from .models import User, Profile, Post, Comment
>>>>>>> a42570f0d471b5cb6a58a386fbef261eec300a57


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]


<<<<<<< HEAD
# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
=======
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


class SignUpForm(UserCreationForm):
    # email = forms.EmailField(required=True)
>>>>>>> a42570f0d471b5cb6a58a386fbef261eec300a57

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)
<<<<<<< HEAD
=======


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'birth_date', 'bio', 'location', 'gender']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class UpdateBlog(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
>>>>>>> a42570f0d471b5cb6a58a386fbef261eec300a57
