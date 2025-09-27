# api/serializers.py
"""
Serializers expose model data to the API layer.

- BookSerializer: serializes Book fields and validates publication_year.
- AuthorSerializer: includes nested books (BookSerializer many=True, read_only=True).
  This leverages the reverse relation Author.books defined by Book.author(related_name='books').
"""
import datetime
from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializes all Book fields.
    Adds field-level validation for publication_year:
      - must not be in the future.
      - must be a positive integer.
    """
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value: int) -> int:
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        if value <= 0:
            raise serializers.ValidationError("Publication year must be a positive integer.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes an Author with a nested, read-only list of their books.

    Because Book.author uses related_name='books', DRF can access author.books
    directly and render each Book using BookSerializer.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
