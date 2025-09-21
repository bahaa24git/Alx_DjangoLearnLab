from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet, health
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path("health/", health, name="health"),    
    path("auth/token/", obtain_auth_token, name="api-token"),
    path("books/", BookList.as_view(), name="book-list"),
    path("", include(router.urls)),                 
    path("auth/", include("rest_framework.urls")),
]