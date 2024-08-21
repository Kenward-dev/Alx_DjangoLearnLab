from bookshelf.models import Book

#book instance
book = Book.objects.get(pk=1)
book.title = "Nineteen Eighty-Four"
book.save()

#expected output
<Book: Nineteen Eighty-Four>