from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    books=Book.objects.all()
    authors = Author.objects.all()
    book_instance = BookInstance.objects.all()
    genres = Genre.objects.all()
    languages = Language.objects.all()
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits']=num_visits+1
    return render(request, "books/index.html",{
        'books': books,
        'authors': authors,
        'book_instance': book_instance,
        'genres': genres,
        'languages': languages,
        'num_visits': num_visits
    })