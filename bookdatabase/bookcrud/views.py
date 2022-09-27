from django.shortcuts import render
from .models import BooksappBook
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Render
def index(request):
    books = BooksappBook.objects.all()

    paginator = Paginator(books, 3)
    page = request.GET.get("page")

    try:
        page_books = paginator.get_page(page)
    except PageNotAnInteger:
        page_books = paginator.get_page(1)
    except EmptyPage:
        page_books = paginator.get_page(paginator.num_pages)

    for book in page_books:
        print(book.book_name)

    data = {"page": page, "page_books": page_books}

    return render(request, "index.html", context=data)

# Create
def create(request):
    if request.method == "GET":
        return render(request, "create.html")
    book = BooksappBook()
    book.book_name = request.POST.get("book_name")
    book.author_name = request.POST.get("author_name")
    book.price = request.POST.get("price")
    book.save()
    return HttpResponseRedirect("/")

# Edit
def edit(request, id):
    try:
        book = BooksappBook.objects.get(id=id)

        if request.method == "POST":
            book.book_name = request.POST.get("book_name")
            book.author_name = request.POST.get("author_name")
            book.price = request.POST.get("price")
            book.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"book": book})
    except BooksappBook.DoesNotExist:
        return HttpResponseNotFound("<h2>Book doesnt exist</h2>")

# Delete
def delete(request, id):
    try:
        book = BooksappBook.objects.get(id=id)
        book.delete()
        return HttpResponseRedirect("/")
    except BooksappBook.DoesNotExist:
        return HttpResponseNotFound("<h2>Book doesnt exist</h2>")
