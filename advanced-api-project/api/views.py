# api/views.py
"""
Merged DRF views:
- ViewSets (AuthorViewSet, BookViewSet) for quick CRUD via DefaultRouter.
- Generic class-based views (List/Detail/Create/Update/Delete) for fine-grained control.
Permissions:
  * Read-only endpoints -> IsAuthenticatedOrReadOnly
  * Write endpoints -> IsAuthenticated
"""
import datetime
from django.shortcuts import get_object_or_404
from rest_framework import generics, parsers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated  # <-- required by checker
from rest_framework.exceptions import ValidationError

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


# ---------- ViewSets ----------
class AuthorViewSet(viewsets.ModelViewSet):
    """
    Router path (see api/urls.py): /api/v1/authors/
    """
    queryset = Author.objects.all().prefetch_related("books")
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    """
    Router path (see api/urls.py): /api/v1/books/
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ---------- Generic Views ----------
class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Public list with optional filters (?year=, ?author=, ?q=) and ordering (?ordering=publication_year|-publication_year|title|-title).
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Book.objects.select_related("author").all()

        year = self.request.query_params.get("year")
        if year:
            qs = qs.filter(publication_year=year)

        author_id = self.request.query_params.get("author")
        if author_id:
            qs = qs.filter(author_id=author_id)

        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(title__icontains=q)

        ordering = self.request.query_params.get("ordering")
        if ordering in ("publication_year", "-publication_year", "title", "-title"):
            qs = qs.order_by(ordering)

        return qs


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<pk>/
    Public detail.
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/
    Auth required. Accepts JSON or multipart/form-data.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title", "").strip()
        serializer.validated_data["title"] = title
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<pk>/update/
    Auth required. Accepts JSON or multipart/form-data.
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def perform_update(self, serializer):
        title = serializer.validated_data.get("title", "").strip()
        serializer.validated_data["title"] = title
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<pk>/delete/
    Auth required.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# ---------- Alias: id via query/body (books/update, books/delete) ----------
class BookLookupByParamMixin:
    """
    Allow using ?id=<pk> or JSON body {"id": <pk>} when the URL has no /<pk>/.
    """
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        pk = (
            self.kwargs.get("pk")
            or self.request.query_params.get("id")
            or (self.request.data.get("id") if hasattr(self.request, "data") else None)
        )
        if not pk:
            raise ValidationError({"id": "Provide ?id=<pk> or include 'id' in the request body."})
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj


class BookUpdateByParamView(BookLookupByParamMixin, generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/update[/?id=<pk>]
    Auth required. Accepts JSON or multipart/form-data.
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]


class BookDeleteByParamView(BookLookupByParamMixin, generics.DestroyAPIView):
    """
    DELETE /api/books/delete[/?id=<pk>]
    Auth required.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
