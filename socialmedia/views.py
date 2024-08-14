from django.shortcuts import render, redirect
from django.views.generic import TemplateView
# from django.views import View
from .models import Profile, Post, Comment


class Home(TemplateView):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)


class LoginSignup(TemplateView):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)


class UserProfile(TemplateView):
    template_name = "user/profile.html"

    def get(self, request):
        data = Profile.objects.all().first()
        context = {
            "data": data
        }
        return render(request, self.template_name, context)


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
        post = Post.objects.filter(id=pk).first()
        comments = Comment.objects.filter(post=post)
        context = {
            "post": post,
            "comments": comments
        }
        return render(request, self.template_name, context=context)


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