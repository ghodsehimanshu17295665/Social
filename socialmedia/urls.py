from django.urls import path
from .views import Home, LoginSignup, UserProfile, BlogList, ViewBlog, AddCommentView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', Home.as_view(), name='home_page'),
    path('login/', LoginSignup.as_view(), name='login_signup'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('blog/list/', BlogList.as_view(), name='blog_list'),
    path('blog/<uuid:pk>/', ViewBlog.as_view(), name='blogview'),
    path('blog/<uuid:pk>/add_comment/', AddCommentView.as_view(), name='add_comment'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
