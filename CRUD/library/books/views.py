from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book

# Create your views here.
class BookListView(ListView):
    model = Book

class BookDetailView(DetailView):
    model = Book

class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'published_date', 'isbn', 'price']

class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'published_date', 'isbn', 'price']

class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('book-list')