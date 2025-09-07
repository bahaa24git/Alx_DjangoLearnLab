# relationship_app/query_samples.py
import os
import sys
import pathlib
import django

# ── Make sure Python can import the settings package "LibraryProject"
# This file is: .../django-models/LibraryProject/relationship_app/query_samples.py
CURRENT_FILE = pathlib.Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent           # .../django-models/LibraryProject
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ── Use your actual settings package name (matches the folder that has settings.py)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")

django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def seed():
    """Create sample data to test queries."""
    a1, _ = Author.objects.get_or_create(name="Naguib Mahfouz")
    a2, _ = Author.objects.get_or_create(name="Ahmed Khaled Tawfik")

    b1, _ = Book.objects.get_or_create(title="Cairo Stories", author=a1)
    b2, _ = Book.objects.get_or_create(title="Palace Walk", author=a1)
    b3, _ = Book.objects.get_or_create(title="Utopia", author=a2)

    lib, _ = Library.objects.get_or_create(name="Downtown Library")
    lib.books.add(b1, b3)

    Librarian.objects.get_or_create(name="Sara Ali", library=lib)


def books_by_author(author_name: str):
    return Book.objects.filter(author__name=author_name)


def books_in_library(library_name: str):
    return Book.objects.filter(libraries__name=library_name).distinct()


def librarian_for_library(library_name: str):
    return Librarian.objects.select_related('library').get(library__name=library_name)


if __name__ == "__main__":
    seed()

    print("Books by Naguib Mahfouz:")
    for b in books_by_author("Naguib Mahfouz"):
        print(" -", b)

    print("\nBooks in Downtown Library:")
    for b in books_in_library("Downtown Library"):
        print(" -", b)

    print("\nLibrarian for Downtown Library:")
    print(librarian_for_library("Downtown Library"))
