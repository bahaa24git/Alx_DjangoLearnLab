from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, BookListView, LibraryDetailView, register, login_view, logout_view

urlpatterns = [
    # Book URLs
    path("books/", list_books, name="list_books"),
    path("books/class/", BookListView.as_view(), name="book_list"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Authentication URLs
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
