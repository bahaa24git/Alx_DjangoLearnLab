from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView,
    register_view, profile_view,
)

app_name = 'blog'

urlpatterns = [
    path('',          PostListView.as_view(),   name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    # auth
    path('login/',      auth_views.LoginView.as_view(template_name='blog/login.html'),      name='login'),
    path('logout/',     auth_views.LogoutView.as_view(template_name='blog/logout.html'),    name='logout'),
    path('register/',   register_view,   name='register'),
    path('profile/',    profile_view,    name='profile'),
    # Posts CRUD
    path('',                         PostListView.as_view(),     name='post_list'),               # list on homepage (keep)
    path('post/<int:pk>/',           PostDetailView.as_view(),   name='post_detail'),
    path('post/new/',                PostCreateView.as_view(),   name='post_create'),          # REQUIRED
    path('post/<int:pk>/update/',    PostUpdateView.as_view(),   name='post_update'),  # REQUIRED
    path('post/<int:pk>/delete/',    PostDeleteView.as_view(),   name='post_delete'),  # REQUIRED
]

