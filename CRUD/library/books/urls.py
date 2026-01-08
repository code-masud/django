from django.urls import path
from . import views
urlpatterns = [
    path('', views.BookListView.as_view(), name='book-list'),
    path('<int:pk>/book/', views.BookDetailView.as_view(), name='book-detail'),
    path('/add/book/', views.BookCreateView.as_view(), name='book-create'),
    path('/edit/book/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),
    path('/delete/book/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),
]