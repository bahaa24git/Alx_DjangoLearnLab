from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, BookListView, register_view

urlpatterns = [
    path("books/", views.list_books, name="list_books"),
    path("books/class/", views.BookListView.as_view(), name="book_list"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
    
    # Authentication URLs
    path("register/", views.register, name="register"),  # renamed view to 'register'
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
