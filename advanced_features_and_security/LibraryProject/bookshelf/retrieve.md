from bookshelf.models import Book
b = Book.objects.get(title="1984", author="George Orwell", publication_year=1949)
(b.title, b.author, b.publication_year)  # ('1984','George Orwell',1949)
