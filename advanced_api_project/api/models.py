from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# A ForeignKey to create a one-to-many relationship between the Book and Author models.
# The related_name='books' allows us to access the books related to an author (e.g., author.books.all()).
# on_delete=models.CASCADE means that if the referenced Author is deleted, the related books will also be deleted.

class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
