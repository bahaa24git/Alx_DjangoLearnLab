from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, BookListView, register_view

urlpatterns = [
    # Book views
    path("books/", list_books, name="list_books"),
    path("class-books/", BookListView.as_view(), name="class_list_books"),

    # Authentication
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name='relationship_app/login.html'), name="login"),
    path("logout/", LogoutView.as_view(template_name='relationship_app/logout.html'), name="logout"),
    
]
