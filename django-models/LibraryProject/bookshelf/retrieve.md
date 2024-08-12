from bookshelf.models import Book

#book instance
book = Book.objects.get(pk=1)

#expected output
<Book: 1984>