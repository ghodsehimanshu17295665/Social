from django import forms
# from socialmedia.models import Post
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# from django.contrib.auth.models import User
from .models import Comment, Post, Profile, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


class SignUpForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture", "birth_date", "bio", "location", "gender"]
        widgets = {
            "profile_picture": forms.ClearableFileInput(
                attrs={"class": "form-control-file", "style": "max-width: 100%;"}
            ),
            "birth_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "style": "max-width: 100%;",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Tell us something about yourself...",
                    "style": "max-width: 100%;",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your location",
                    "style": "max-width: 100%;",
                }
            ),
            "gender": forms.Select(
                attrs={"class": "form-control", "style": "max-width: 100%;"}
            ),
        }


class UpdateBlog(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the title",
                    "style": "max-width: 100%;",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your content here...",
                    "rows": 5,
                    "style": "max-width: 100%;",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control-file", "style": "max-width: 100%;"}
            ),
        }


# class ChangePasswordForm(forms.Form):
#     old_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter old password',
#             'style': 'max-width: 100%;'
#         })
#     )
#     new_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter new password',
#             'style': 'max-width: 100%;'
#         })
#     )
#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Confirm new password',
#             'style': 'max-width: 100%;'
#         })
#     )
