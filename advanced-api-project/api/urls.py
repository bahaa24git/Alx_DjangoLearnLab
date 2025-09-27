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
    path("books/update/", BookUpdateByParamView.as_view(), name="book-update-no-pk"),
    path("books/delete/", BookDeleteByParamView.as_view(), name="book-delete-no-pk"),

    # ViewSets (router)
    path("v1/", include(router.urls)),
]
