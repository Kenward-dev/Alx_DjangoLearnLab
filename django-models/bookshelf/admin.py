from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ['title', 'author']
    search_fields = ['title, author', 'publication_year']

admin.site.register(Book, BookAdmin)