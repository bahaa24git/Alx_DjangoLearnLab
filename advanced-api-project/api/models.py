# api/models.py
from django.db import models

class Author(models.Model):
    """
    Represents a writer/creator.
    One Author -> Many Books (see Book.author ForeignKey below).
    """
    name = models.CharField(
        max_length=255,
        help_text="Human-readable name of the author."
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a publication written by an Author.
    The ForeignKey with related_name='books' gives us Author.books for reverse access.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField(help_text="Gregorian year of publication.")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",  # enables nested serialization via author.books
    )

    class Meta:
        ordering = ["publication_year", "title"]

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
