from django.urls import path
from .views import list_books, LibraryDetailView


urlpatterns = [
    path("books/", list_books, name="list-books"),                          # FBV
    path("libraries/<int:pk>/", LibraryDetailView.as_view(),
         name="library-detail"),  # CBV

    path("login/",  LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),
    path("roles/admin/", views.admin_view, name="admin-view"),
    path("roles/librarian/", views.librarian_view, name="librarian-view"),
    path("roles/member/", views.member_view, name="member-view"),
    path("books/add/", views.add_book, name="book-add"),
    path("books/<int:pk>/edit/", views.edit_book, name="book-edit"),
    path("books/<int:pk>/delete/", views.delete_book, name="book-delete"),
    path("add_book/", views.add_book, name="add_book"),
    path("edit_book/<int:pk>/", views.edit_book, name="edit_book"),
    path("delete_book/<int:pk>/", views.delete_book, name="delete_book"),
]
