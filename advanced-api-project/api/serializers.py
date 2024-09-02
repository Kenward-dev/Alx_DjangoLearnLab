from .models import Book
from .models import Author
from rest_framework import serializers
import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    # Define a custom validation method for the publication_date field.
    def validate_publication_year(self, value):
        # Check if the provided publication_date is in the future.
        if value > datetime.date.today().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    # The books field uses the BookSerializer to serialize related Book objects.
    # many=True indicates that multiple books can be associated with an author.
    # read_only=True means this field is only for display purposes and won't be used for input.

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']