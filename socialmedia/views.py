from django.shortcuts import render, redirect
from django.views.generic import TemplateView
# from django.views import View
from .models import Profile, Post, Comment
from django.shortcuts import get_object_or_404


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


class Blog(TemplateView):
    template_name = "user/blog.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')

        posts = Post.objects.all()
        context = {
            "posts": posts
        }
        return render(request, self.template_name, context=context)


class AddCommentView(TemplateView):
    template_name = "user/blog.html"

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(post=post, user=request.user, comment=comment_text)
        return redirect('/')


# class AddCommentView(View):
#     def post(self, request, pk):
#         try:
#             post = Post.objects.get(id=uuid.UUID(pk))
#         except Post.DoesNotExist:
#             return redirect('blog_list')  # Redirect if post does not exist

#         comment_text = request.POST.get('comment')
#         if comment_text:
#             Comment.objects.create(post=post, user=request.user, comment=comment_text)

#         return redirect('blog_list')

