from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from .models import UserProfile
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required


def list_books(request):
    books = Book.objects.all()
    list_book = [f"{book.title} by {book.author}" for book in books]
    return render(request, 'relationship_app/list_books.html', {'list_book': list_book})

@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        # handle book addition
        pass
    return render(request, 'relationship_app/add_book.html')

@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        # handle book editing
        pass
    return render(request, 'relationship_app/edit_book.html', {'book': book})

@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        # handle book deletion
        pass
    return render(request, 'relationship_app/delete_book.html', {'book': book})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context
class register(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Determine the redirect URL based on the user's role
            if user.userprofile.role == 'Admin':
                return redirect('admin_view')
            elif user.userprofile.role == 'Librarian':
                return redirect('librarian_view')
            else:
                return redirect('member_view')
            
    # If the form is not valid, re-render the registration form with errors
        return render(request, 'relationship_app/register.html', {'form': form})

    
    
def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'

# Admin View
@user_passes_test(is_admin)
def admin_view(request):
    context = {
        'role': 'Admin',
        'message': 'Welcome to the Admin Dashboard',
        'total_books': Book.objects.count(),
        'total_members': UserProfile.objects.filter(role='Member').count(),
        'total_librarians': UserProfile.objects.filter(role='Librarian').count(),
    }
    return render(request, 'relationship_app/admin_view.html', context)

# Librarian View
@user_passes_test(is_librarian)
def librarian_view(request):
    context = {
        'role': 'Librarian',
        'message': 'Welcome to the Librarian Dashboard'
    }
    return render(request, 'relationship_app/librarian_view.html', context)

# Member View
@user_passes_test(is_member)
def member_view(request):
    context = {
        'role': 'Member',
        'message': 'Welcome to the Member Dashboard'
    }
    return render(request, 'relationship_app/member_view.html', context)
