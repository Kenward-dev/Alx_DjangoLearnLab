from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.models import Group, Permission
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fielsets = (
        (None, {'fields': ('username', 'password')}),
        ('Details', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        ('activity_dates', {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')

# Create groups and assign permissions
editors_group, created = Group.objects.get_or_create(name='Editors')
editors_group.permissions.add(
    Permission.objects.get(codename='can_create_book'),
    Permission.objects.get(codename='can_edit_book'),
)

viewers_group, created = Group.objects.get_or_create(name='Viewers')
viewers_group.permissions.add(
    Permission.objects.get(codename='can_view_book'),
)

admins_group, created = Group.objects.get_or_create(name='Admins')
admins_group.permissions.add(
    Permission.objects.get(codename='can_view_book'),
    Permission.objects.get(codename='can_create_book'),
    Permission.objects.get(codename='can_edit_book'),
    Permission.objects.get(codename='can_delete_book'),
)