from django.urls import path
from .views import PostListView, PostDetailView
from django.contrib.auth import views as auth_views
from .views import PostListView, PostDetailView, register_view, profile_view
app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    # auth
    path('login/',  auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
]

