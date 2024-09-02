from .models import Book
from .models import Author
from .seriealizers import BookSerializer
from .seriealizers import AuthorSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (
    ListAPIView, 
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
    )

# ListView for retrieving all books
class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Allow read-only access
    permission_classes = [AllowAny]  

# DetailView for retrieving a single book by ID
class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Allow read-only access
    permission_classes = [AllowAny]

# CreateView for adding a new book
class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Restrict access to authenticated users
    permission_classes = [IsAuthenticated]  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# UpdateView for modifying an existing book
class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Restrict access to authenticated users
    permission_classes = [IsAuthenticated]

# DeleteView for removing a book
class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()

    # Restrict access to authenticated users
    permission_classes = [IsAuthenticated]
