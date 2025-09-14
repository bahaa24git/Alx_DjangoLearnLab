from django.urls import path
from django.contrib.auth import views as auth_views
from .views import list_books, BookListView, register_view, login_view, logout_view, LibraryDetailView

urlpatterns = [
    # Book views
    path("books/", list_books, name="list_books"),
    path("class-books/", BookListView.as_view(), name="class_list_books"),

    # Authentication
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

]
