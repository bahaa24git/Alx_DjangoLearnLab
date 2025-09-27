# api/views.py
"""
Merged DRF views:
- ViewSets (AuthorViewSet, BookViewSet) for quick, full CRUD routing via DefaultRouter.
- Generic class-based views (List/Detail/Create/Update/Delete) for fine-grained control.
  * Read-only endpoints (List/Detail) are public.
  * Write endpoints (Create/Update/Delete) require authentication.
  * Create/Update accept JSON and multipart/form-data.
  * List supports filtering (?year=, ?author=, ?q=) and ordering (?ordering=publication_year|-publication_year|title|-title).
"""
from rest_framework import generics, permissions, parsers, viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


# ---------- ViewSets (fast, router-based CRUD) ----------
class AuthorViewSet(viewsets.ModelViewSet):
    """
    Router path (see api/urls.py):
      /api/v1/authors/
    """
    queryset = Author.objects.all().prefetch_related("books")
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    Router path (see api/urls.py):
      /api/v1/books/
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer


# ---------- Generic Views (explicit endpoints & behaviors) ----------
class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Public list with optional filters and ordering.
    Filters:
      - ?year=YYYY
      - ?author=<author_id>
      - ?q=<title contains>
    Ordering:
      - ?ordering=publication_year | -publication_year | title | -title
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

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
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/
    Auth required. Accepts JSON or multipart/form-data.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def perform_create(self, serializer):
        # Light sanitation + rely on BookSerializer validation for publication_year
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
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
