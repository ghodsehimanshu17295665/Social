from django.urls import path
from .views import Home, Login, UserProfile, BlogList, ViewBlog, AddCommentView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', Home.as_view(), name='home_page'),
    path('login/', Login.as_view(), name='login'),
    # path('signup/', Signup.as_view(), name='signup'),
    path('blog/list/', BlogList.as_view(), name='blog_list'),
    path('blog/<uuid:pk>/', ViewBlog.as_view(), name='blogview'),
    path('blog/<uuid:pk>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('profile/<uuid:pk>/', UserProfile.as_view(), name='profile'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
