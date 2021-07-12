from django.urls import path
from django.views.generic.detail import DetailView
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='blog-about'),
    path('upload/', views.upload, name='upload'),
    # path(r'^upload/csv/$', views.upload_csv, name='upload_csv'),
    # url(r'^user/(?P<username>\w{0,50})/$', UserPostListView.as_view(), name='user-posts'),
]