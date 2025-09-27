# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # ViewSets
    AuthorViewSet, BookViewSet,
    # Generic views
    BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView,
)

# ViewSets under /api/v1/... to avoid collisions with the generic endpoints
router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"books", BookViewSet, basename="book")

urlpatterns = [
    # Generic views (explicit endpoints)
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),

    # ViewSets (router)
    path("v1/", include(router.urls)),
]
