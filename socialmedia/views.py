from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.views.generic import DetailView
from django.contrib import messages
from .models import Profile, Post, Comment, Like
from .forms import SignUpForm, ProfileUpdateForm, PostForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout


class Home(TemplateView):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)


# class Signup(TemplateView):
#     template_name = "registration/signup.html"

#     def get(self, request):
#         return render(request, self.template_name)


# class Login(TemplateView):
#     template_name = "registration/login.html"

#     def get(self, request):
#         return render(request, self.template_name)


class BlogList(TemplateView):
    template_name = "user/blog_list.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/login/")

        posts = Post.objects.all()
        context = {"posts": posts}
        return render(request, self.template_name, context=context)


class ViewBlog(TemplateView):
    template_name = "user/Viewblog.html"

    def get(self, request, pk):
        post = Post.objects.get(id=pk)

        comments = Comment.objects.filter(post=post)
        context = {
            "post": post,
            "comments": comments,
        }
        return render(request, self.template_name, context=context)


class UserProfile(TemplateView):
    template_name = "user/profile.html"

    def get(self, request, pk):
        data = Profile.objects.filter(user=pk).first()
        context = {
            "data": data,
        }
        return render(request, self.template_name, context)


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


class LikePostView(View):
    def post(self, request, pk):
        # Use .get() to retrieve the post
        post = Post.objects.filter(id=pk).first()

        if post is None:
            # Handle the case where the post doesn't exist
            return redirect(
                "home_page"
            )  # Redirect to the homepage or any other appropriate page

        # Use get_or_create to handle like/unlike logic
        like, created = Like.objects.get_or_create(
            user=request.user, post=post
        )

        if not created:
            # If the like already exists, delete it (unlike action)
            like.delete()

        return redirect("blogview", pk=post.id)


# SignUp View Function
class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                # profile_picture='img/default_profile_pic.jpg',
                birth_date=None,
                bio=None,
                location=None,
                gender=None,
            )
            messages.success(request, "Account created successfully! You are now logged in.")
            return redirect('/')
        return render(request, 'registration/signup.html', {'form': form})


# Login View Function
class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/profile/page/')
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_password = form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in Successfully!!')
                return redirect('/profile/page/')
            else:
                form.add_error(None, 'Invalid username or password')
        return render(request, 'registration/login.html', {'form': form})


# Profile
class UserProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')

        # Retrieve the user's profile
        data = Profile.objects.filter(user=request.user).first()
        context = {"data": data}
        return render(request, "registration/profilepage.html", context)


# Logout
class LogoutView(View):
    template_name = "registration/logout_confirmation.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logout(request)
        return redirect("/")


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
