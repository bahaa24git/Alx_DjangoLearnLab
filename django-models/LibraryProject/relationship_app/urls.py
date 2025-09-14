from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("relationship_app.urls")),
    # Function-based view
    path("books/", views.list_books, name="list_books"),

    # Class-based view
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
]