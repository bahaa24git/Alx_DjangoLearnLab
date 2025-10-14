# DELETE

```python
from bookshelf.models import Book
count_before = Book.objects.count()
book = Book.objects.get(title="Nineteen Eighty-Four", author="George Orwell", publication_year=1949)
book.delete()
count_after = Book.objects.count()
(count_before, count_after)
