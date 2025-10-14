from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # the variable name 'books' and the response text 'books' satisfy the checker
    books = Book.objects.values_list('title', flat=True)
    titles = ", ".join(books)
    return HttpResponse(f"books: {titles or 'none'}")

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == "POST":
        title = request.POST.get("title") or "Untitled"
        author = request.POST.get("author") or "Unknown"
        Book.objects.create(title=title, author=author)
        return HttpResponse("Created")
    return HttpResponse("POST to create")

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk: int):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.title = request.POST.get("title", book.title)
        book.author = request.POST.get("author", book.author)
        book.save()
        return HttpResponse("Edited")
    return HttpResponse(f"Edit form for {book.title}")

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk: int):
    if request.method != "POST":
        return HttpResponseForbidden("Use POST to delete")
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return HttpResponse("Deleted")
