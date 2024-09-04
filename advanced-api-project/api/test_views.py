from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Book, Author
from django.core.management import call_command
from rest_framework import status

class BookTestCase(APITestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create an author
        self.author = Author.objects.create(name='Chinua Achebe')

        # Create a book
        self.book = Book.objects.create(title='Things Fall Apart', publication_year=1958, author=self.author)

    def test_create_book(self):
        url = reverse('book-create')
        data = {'title': 'New Book', 'publication_year': 2024, 'author': self.author.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # HTTP 201 Created
        self.assertEqual(Book.objects.count(), 2)  # Check if the book count increased

    def test_read_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # HTTP 200 OK
        self.assertContains(response, 'Things Fall Apart')  # Check if the response contains the book title

    def test_update_book(self):
        url = reverse('book-update', kwargs={'pk': self.book.pk})
        data = {'title': 'Updated Book', 'publication_year': 2023, 'author': self.author.id}
        response = self.client.put(url, data, content_type='application/json')  # Ensure correct content type

        # Use debug_response() to get more information about the response
        call_command('debug_response', response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # HTTP 200 OK
        self.assertEqual(response.data['title'], 'Updated Book')  # Check if the book title was updated
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_delete_book(self):
        url = reverse('book-delete', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)  # Use DELETE for removing
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # HTTP 204 No Content
        self.assertEqual(Book.objects.count(), 0)  # Check if the book was deleted

    def test_filter_books(self):
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'Things Fall Apart'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one book should match the filter

    def test_search_books(self):
        url = reverse('book-list')

        # Searching by book title
        response = self.client.get(url, {'title__icontains': 'Things'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Things Fall Apart')

        # Searching by author name
        response = self.client.get(url, {'author__name__icontains': 'Achebe'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Things Fall Apart')

    def test_order_books(self):
        # Add another book to test ordering
        Book.objects.create(title='Another Book', publication_year=2000, author=self.author)

        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = response.data

        # Ensure publication_year is not None before comparison
        valid_books = [book for book in books if book['publication_year'] is not None]
        self.assertTrue(all(valid_books[i]['publication_year'] <= valid_books[i+1]['publication_year']
                        for i in range(len(valid_books)-1)))

    def test_permissions(self):
        # Testing without login (should be forbidden)
        self.client.logout()
        url = reverse('book-create')
        data = {'title': 'New Book', 'publication_year': 2024, 'author': self.author.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # HTTP 403 Forbidden for unauthenticated user

        # Testing with login (should be successful)
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # HTTP 201 Created