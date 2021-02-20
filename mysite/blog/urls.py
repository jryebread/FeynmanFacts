from django.urls import path
from . import views
from .views import PostListView, PostListSearchView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('searchPosts', PostListSearchView.as_view(), name="search_posts"),
    path('post/like/<int:pk>/', views.send_like, name='like_post'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), 
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), 
    path('about', views.about, name='blog-about')
]