from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from .models import UserProfile
from django.views import View
from django.contrib.auth.decorators import user_passes_test

def list_books(request):
    books = Book.objects.all()
    list_book = [f"{book.title} by {book.author}" for book in books]
    return render(request, 'relationship_app/list_books.html', {'list_book': list_book})

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
            UserProfile.objects.create(user=user, role='Member')
            return redirect('login')  
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
        'message': 'Welcome to the Admin Dashboard'
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
