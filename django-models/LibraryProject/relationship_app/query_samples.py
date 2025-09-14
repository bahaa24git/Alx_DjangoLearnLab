import os
import sys
import django

# Add project directory (LibraryProject) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Point to Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

# Setup Django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

print("=== Query Samples ===\n")

# 1. List all authors
print("📚 Authors:")
for author in Author.objects.all():
    print(f" - {author.name}")

# 2. List all books
print("\n📖 Books:")
for book in Book.objects.all():
    print(f" - {book.title} (Author: {book.author.name})")

# 3. List all libraries and their books
print("\n🏛️ Libraries and their books:")
for library in Library.objects.all():
    print(f" - {library.name}")
    for book in library.books.all():
        print(f"   * {book.title}")

# 4. List all librarians and their libraries
print("\n👩‍💼 Librarians:")
for librarian in Librarian.objects.all():
    print(f" - {librarian.name} (Library: {librarian.library.name})")

# 5. Example query: find all books by J.K. Rowling
print("\n🔎 Books by J.K. Rowling:")
jk_books = Book.objects.filter(author__name="J.K. Rowling")
for book in jk_books:
    print(f" - {book.title}")

print("\n✅ Query samples executed successfully!")
