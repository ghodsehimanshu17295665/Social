from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, View

from .email_utils import send_verification_email
from .forms import (CommentForm, PostForm, ProfileUpdateForm, SignUpForm,
                    UpdateBlog)
from .models import Comment, Follow, Like, Post, Profile, User


class Home(TemplateView):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)


# SignUp View Function
class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        form = SignUpForm()
        return render(request, "registration/signup.html", {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                birth_date=None,
                bio=None,
                location=None,
                gender=None,
            )
            send_verification_email(user, request)
            messages.success(
                request, "Account created successfully! You are now logged in."
            )
            return redirect("login")
        return render(request, "registration/signup.html", {"form": form})


# Login View Function
class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/profile/page/")
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["username"]
            user_password = form.cleaned_data["password"]
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
                if not user.email_verified:
                    if user.is_token_valid():
                        login(request, user)
                        messages.success(request, "Logged in Successfully!!")
                        return redirect("/profile/page/")
                    else:
                        user.generate_verification_token()
                        send_verification_email(user, request)
                        messages.error(
                            request,
                            "your email verification link has expire. A new verification link has been sent to your email.",
                        )
                        return redirect("login")
                else:
                    login(request, user)
                    return redirect("/profile/page/")
            else:
                form.add_error(None, "Invalid username or password")
        return render(request, "registration/login.html", {"form": form})


# Activate Account View
class ActivateAccountView(View):
    def get(self, request, uid, token):
        user = User.objects.filter(id=uid, verification_token=token).first()

        if user and user.is_token_valid():
            user.email_verified = True
            user.verification_token = None
            user.token_created_at = None
            user.save()
            messages.success(
                request,
                "Thank you for verifying your email. You can now log in.",
            )
            return redirect("login")
        elif user:
            user.generate_verification_token()
            send_verification_email(user, request)
            messages.error(
                request,
                "Your email verification link has expired. A new verification link has been sent to your email.",
            )
            return redirect("login")
        else:
            messages.error(request, "Invalid verification link.")
            return redirect("login")


# Logout
class LogoutView(View):
    template_name = "registration/logout_confirmation.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logout(request)
        return redirect("/")


# Profile
class UserProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/login/")

        data = Profile.objects.filter(user=request.user).first()
        context = {"data": data}
        return render(request, "registration/profilepage.html", context)


# Update Profile Page:-
class UpdateProfile(TemplateView):
    template_name = "registration/updateprofile.html"

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        form = ProfileUpdateForm(instance=profile)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your profile has been updated successfully!"
            )
            return redirect("/profile/page/")
        else:
            messages.error(request, "Please correct the errors below.")
        return render(request, self.template_name, {"form": form})


# Create Blog:-
class CreatePost(TemplateView):
    template_name = "registration/createPost.html"

    def get(self, request):
        form = PostForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(
                request, "Your post has been created successfully!"
            )
            return redirect("post_detail", pk=post.pk)
        else:
            messages.error(request, "Please correct the errors below.")
        return render(request, self.template_name, {"form": form})


class PostDetailView(DetailView):
    model = Post
    template_name = "registration/post_detail.html"
    context_object_name = "post"


# Update Blog:-
class Updateblog(TemplateView):
    template_name = "registration/blogupdate.html"

    def get(self, request, pk):
        post = Post.objects.filter(id=pk).first()
        if post:
            form = UpdateBlog(instance=post)
            return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        post = Post.objects.filter(id=pk).first()
        if post:
            form = UpdateBlog(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, "Blog updated successfully.")
                return render(request, self.template_name, {"form": form})


# List User Blog:-
class Myblog(TemplateView):
    template_name = "user/myblog.html"

    def get(self, request):
        posts = Post.objects.filter(user=request.user)
        context = {"posts": posts}
        return render(request, self.template_name, context=context)


# List All Blog.
class BlogList(TemplateView):
    template_name = "user/blog_list.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/login/")

        posts = Post.objects.all()
        context = {"posts": posts}
        return render(request, self.template_name, context=context)


# View Blog:-
class ViewBlog(TemplateView):
    template_name = "user/Viewblog.html"

    def get(self, request, pk):
        post = Post.objects.filter(pk=pk).first()

        comments = Comment.objects.filter(post=post)
        context = {
            "post": post,
            "comments": comments,
        }
        return render(request, self.template_name, context=context)


class UserProfile(TemplateView):
    template_name = "user/profile.html"

    def get(self, request, pk):
        user = User.objects.filter(id=pk).first()
        data = Profile.objects.filter(user=user).first()
        context = {
            "data": data,
        }
        return render(request, self.template_name, context)


# Add Comment in Blog:-
class AddCommentView(TemplateView):
    template_name = "user/Viewblog.html"

    def get(self, request, pk):
        post = Post.objects.filter(id=pk).first()
        comments = Comment.objects.filter(post=post)
        form = CommentForm()
        context = {"post": post, "comments": comments, "form": form}
        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        post = Post.objects.filter(id=pk).first()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect("add_comment", pk=pk)

        comments = Comment.objects.filter(post=post)
        context = {"post": post, "comments": comments, "form": form}
        return render(request, self.template_name, context)


# Add Like:-
class LikePostView(View):
    def post(self, request, pk):
        post = Post.objects.filter(id=pk).first()

        if post is None:
            return redirect("home_page")
        like, created = Like.objects.get_or_create(
            user=request.user, post=post
        )

        if not created:
            like.delete()

        return redirect("blogview", pk=post.id)


# Follow:-
class FollowUserView(View):
    def post(self, request, pk):
        user_to_follow = User.objects.filter(pk=pk).first()

        if not user_to_follow:
            return redirect("home_page")

        follow, created = Follow.objects.get_or_create(
            user=request.user, user_following=user_to_follow
        )

        if not created:
            follow.delete()

        return redirect("home_page")


# Change Password
class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profilePage')
    template_name = 'registration/change_password.html'


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
