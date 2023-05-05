from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from books.models import Book


def index_view(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    book = Book.objects.all()
    context = {
        'books': book,
    }
    return render(request, template, context)

def books_date_view(request, date):
    template = 'books/books_list.html'
    book = Book.objects.all().filter(pub_date=date)
    page = Book.objects.values('pub_date')
    context = {
        'books': book,
        'pages': page,
    }
    return render(request, template, context)
