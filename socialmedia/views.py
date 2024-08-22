from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from .models import Profile, Post, Comment
from .forms import SignUpForm, ProfileUpdateForm, PostForm
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


class Login(TemplateView):
    template_name = "registration/login.html"

    def get(self, request):
        return render(request, self.template_name)


class BlogList(TemplateView):
    template_name = "user/blog_list.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')

        posts = Post.objects.all()
        context = {
            "posts": posts
        }
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
    template_name = "user/blog.html"

    def get(self, request, pk):
        post = Post.objects.filter(id=pk).first()
        comments = Comment.objects.filter(post=post)
        print(comments)
        context = {
            "comments": comments
        }
        return render(request, self.template_name, context=context)


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(
                user=user,
                # profile_picture='img/default_profile_pic.jpg',
                birth_date=None,
                bio=None,
                location=None,
                gender=None
            )
            print(f'Profile created: {profile}')  # Debug print
            messages.success(request, "Account created successfully! You are now logged in.")
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# Login View Function
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
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
        else:
            form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    else:
        return redirect('/profile/page/')


# Profile
def user_profile(request):
    if request.user.is_authenticated:
        data = Profile.objects.filter(user=request.user).first()
        print(data)
        context = {
            'data': data
        }
        return render(request, 'registration/profilepage.html', context)
    else:
        return redirect('/login/')


# Logout
def user_logout(request):
    logout(request)
    return redirect('/')


# Update Profile Page:-
class UpdateProfile(TemplateView):
    template_name = 'registration/updateprofile.html'

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        form = ProfileUpdateForm(instance=profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('/profile/page/')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, self.template_name, {'form': form})


# Create Blog:-
class CreatePost(TemplateView):
    template_name = "registration/createPost.html"

    def get(self, request):
        form = PostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('/profile/page/')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, self.template_name, {'form': form})
