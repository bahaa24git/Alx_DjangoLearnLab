from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("books/", views.list_books, name="list_books"),
    path("books/class/", views.BookListView.as_view(), name="book_list"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # Authentication URLs
    path("register/", views.register, name="register"),  # function-based register view
    path("login/", LoginView.as_view(template_name="register.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="register.html"), name="logout"),
]
