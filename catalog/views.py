# from django.shortcuts import get_object_or_404
# from django.shortcuts import render
# from django.http import HttpResponse, Http404
# from django.views import generic
# from .models import Book, Author, BookInstance, Genre, Language
# # Create your views here.


# def index(request):
#     num_books = Book.objects.all().count()
#     num_instances = BookInstance.objects.all().count()

#     num_instances_available = BookInstance.objects.filter(
#         status__exact='a').count()

#     num_authors = Author.objects.count()

#     # challenge
#     num_genres = Genre.objects.count()
#     genres = Genre.objects.all()
#     novels = Book.objects.filter(genre__name__exact='Novel').count()

#     context = {
#         'num_books': num_books,
#         'num_instances': num_instances,
#         'num_instances_available': num_instances_available,
#         'num_authors': num_authors,
#         'num_genres': num_genres,
#         'novels': novels,
#         'genres': genres
#     }
#     return render(request, 'index.html', context=context)


# class BookListView(generic.ListView):
#     model = Book
#     paginate_by = 4
#     # your own name for the list as a template variable

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super(BookListView, self).get_context_data(**kwargs)
#         # Create any data and add it to the context
#         context['sth'] = 'This is just some data'
#         return context

#     def get_queryset(self):
#         return Book.objects.all()
#     # # Specify your own template name/location
#     template_name = 'catalog/book_list.html'


# class BookDetailView(generic.DetailView):
#     model = Book

#     def book_detail_view(request, primary_key):
#         # try:
#         #     book = Book.objects.get(pk=primary_key)
#         # except Book.DoesNotExist:
#         #     raise Http404('Book does not exist')
#         book = get_object_or_404(Book, pk=primary_key)
#         return render(request, 'catalog/book_detail.html', context={'book': book})


# class AuthorListView(generic.ListView):
#     model = Author
#     paginate_by = 5

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super(AuthorListView, self).get_context_data(**kwargs)
#         # Create any data and add it to the context
#         context['sth'] = 'This is just some data'
#         return context

#     def get_queryset(self):
#         return Author.objects.all()
#     # # Specify your own template name/location
#     template_name = 'catalog/author_list.html'


# class AuthorDetailView(generic.DetailView):
#     model = Author

#     def author_detail_view(request, primary_key):
#         author = get_object_or_404(Author, pk=primary_key)
#         return render(request, 'catalog/author_detail.html', context={'author': author})

from django.shortcuts import render
from catalog.models import Book, Author
from catalog.permissions import IsOwnerOrReadOnly
from catalog.serializers import BookSerializer, AuthorSerializer, UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'books': reverse('book-list', request=request, format=format),
    })

######## CLASS-BASED VIEW #########
# class BookList(APIView):
#     """
#     List all books, or create a new book.
#     """

#     def get(self, request, format=None):
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True)
#         return Response(serializer.data)
#         # return render(request, 'catalog/book_list.html', context={'book_list': serializer.data})

#     def post(self, request, format=None):
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class BookDetail(APIView):
#     """
#     Retrieve, update or delete a books instance.
#     """

#     def get_object(self, pk):
#         try:
#             return Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         book = self.get_object(pk)
#         serializer = BookSerializer(book)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         book = self.get_object(pk)
#         serializer = BookSerializer(book, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         book = self.get_object(pk)
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

######### USING MIXINS #########

# class BookList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class BookDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


######### USING GENERIC CLASS-BASED VIEWS #########

class BookList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorList(APIView):
    def get(self, request, format=None):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthorDetail(APIView):
    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
