from django.urls import path
from . import views

urlpatterns = [
    # Book and Library URLs
    path("books/", views.list_books, name="list_books"),
    path("books/class/", views.BookListView.as_view(), name="book_list"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # Authentication URLs
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Role-Based URLs
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),
]
