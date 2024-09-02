from .models import Book
from .models import Author
from .seriealizers import BookSerializer
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics
from django_filters import rest_framework

# ListView for retrieving all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Adding filtering, searching, and ordering backends
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]

    # Fields to search in
    search_fields = ['title', 'author', 'publication_year']

    # Fields to filter by
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Fields to order by
    ordering_fields = ['title', 'publication_date']


    # Allow read-only access
    permission_classes = [IsAuthenticatedOrReadOnly]  

# DetailView for retrieving a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Allow read-only access
    permission_classes = [IsAuthenticatedOrReadOnly]

# CreateView for adding a new book
class BookCreateView(generics.CreateAPIView):
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
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Restrict access to authenticated users
    permission_classes = [IsAuthenticated]

# DeleteView for removing a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()

    # Restrict access to authenticated users
    permission_classes = [IsAuthenticated]
