from django.urls import path
from . import views
from .views import list_books, LibraryDetailView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("relationship_app.urls")),
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]