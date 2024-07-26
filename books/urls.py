from django.urls import path
from . import language_views, author_views, book_views, index_views, book_instance_views, genre_views, class_based_views

urlpatterns=[
    path('', index_views.index, name="index"),
    path('languages', language_views.handleLanguages, name="languages"),
    path('books', book_views.handleBooks, name="books"),
    path('bookInstances', book_instance_views.handleBookInstances, name="book_instances"),
    path('genres', genre_views.handleGenres, name="genres"),
    path('authors', author_views.handleAuthors, name="authors"),
    path('books_list', class_based_views.BookListView.as_view(), name="book_list"),
    path('book_detail/<int:pk>', class_based_views.BookDetailView.as_view(), name='book-detail'),
    path('users', class_based_views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', class_based_views.UserDetailView.as_view(), name='user-detail'),
    path('register', class_based_views.RegisterAPIView.as_view(), name='register'),
    path('login', class_based_views.LoginAPIView.as_view(), name='login'),
    path('getBookInstancesByStatus', book_instance_views.getBookInstancesByStatus, name='book_ins_by_status'),
    path('getBookInstancesLateSubmission', book_instance_views.getBookInstancesLateSubmission, name='book_ins_by_late_sub'),
    path('search_by_title', book_views.search_by_title, name='searh_book_by_title')
]