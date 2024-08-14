from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Post, Comment, Like, Follow


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "profile_picture", "birth_date", "bio", "location", "gender")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content", "image", "user")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "user", "comment")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "user")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "user_following")
