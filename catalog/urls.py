from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from catalog import views

# urlpatterns = [
#         path('', views.index, name='index'),
#         path('books/', views.BookListView.as_view(), name='books'),
#         # path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
#         re_path(r'^book/(?P<pk>\d+)$',
#                 views.BookDetailView.as_view(), name='book-detail'),
#         path("authors/", views.AuthorListView.as_view(), name='authors'),
#         re_path(r'^author/(?P<pk>\d+)$',
#                 views.AuthorDetailView.as_view(), name='author-detail'),
# ]

urlpatterns = [
    path("", views.api_root),
    path('books/', views.BookList.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetail.as_view()),
    path('authors/', views.AuthorList.as_view()),
    path('authors/<int:pk>', views.AuthorDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
