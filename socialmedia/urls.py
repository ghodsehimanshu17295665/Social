from django.urls import path
from .views import Home, LoginSignup, UserProfile, Blog, AddCommentView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', Home.as_view(), name='home_page'),
    path('login/', LoginSignup.as_view(), name='login_signup'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('blog/list/', Blog.as_view(), name='blog_list'),
    path('post/comment/<int:pk>/', AddCommentView.as_view(), name='add_comment'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
