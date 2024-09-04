from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (ActivateAccountView, AddCommentView, BlogList,
                    ChangePasswordView, CreatePost,
                    CustomPasswordResetCompleteView,
                    CustomPasswordResetConfirmView,
                    CustomPasswordResetDoneView, CustomPasswordResetView,
                    FollowUserView, Home, LikePostView, LogoutView, Myblog,
                    PostDetailView, SignUpView, Updateblog, UpdateProfile,
                    UserLoginView, UserProfile, UserProfileView, ViewBlog)

urlpatterns = [
    # Home Page
    path("", Home.as_view(), name="home_page"),
    # signUp/Login/Logout Page
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # User Profile related page
    path("profile/<uuid:pk>/", UserProfile.as_view(), name="profile"),
    path("profile/update/", UpdateProfile.as_view(), name="update_profile"),
    path("create/post/", CreatePost.as_view(), name="create_post"),
    path("post/<uuid:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("blog/update/<uuid:pk>/", Updateblog.as_view(), name="update_blog"),
    # list all user related
    path("my/blog/", Myblog.as_view(), name="my_blog"),
    path("blog/list/", BlogList.as_view(), name="blog_list"),
    path("blog/<uuid:pk>/", ViewBlog.as_view(), name="blogview"),
    path("profile/page/", UserProfileView.as_view(), name="profilePage"),
    path(
        "blog/<uuid:pk>/add_comment/",
        AddCommentView.as_view(),
        name="add_comment",
    ),
    path("post/<uuid:pk>/like/", LikePostView.as_view(), name="like_post"),
    # Follow
    path("follow/<uuid:pk>/", FollowUserView.as_view(), name="follow_user"),
    # email verification
    path(
        "activate/<uuid:uid>/<str:token>/",  # <uuid:uid> for UUID type
        ActivateAccountView.as_view(),
        name="activate",
    ),
    # Change Password
    path(
        "change/password/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    # User-facing password reset views
    path(
        "password_reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
