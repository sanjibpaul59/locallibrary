from rest_framework import serializers
from catalog.models import Book, Author, BookInstance, Genre, Language
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Book.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'books')


class BookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Book
        fields = ['title', 'author_name', 'summary',
                  'isbn', 'display_genre', 'display_language', 'owner']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
