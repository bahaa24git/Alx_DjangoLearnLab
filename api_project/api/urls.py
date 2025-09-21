from django.urls import path
from .views import BookList, health

urlpatterns = [
    path("health/", health, name="health"),      # optional
    path("books/", BookList.as_view(), name="book-list"),
]
