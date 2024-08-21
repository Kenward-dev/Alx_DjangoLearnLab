from bookshelf.models import Book

#book instance
book = Book.objects.get(pk=1)
book.delete()

#expected output
(1, {'bookshelf.Book': 1})