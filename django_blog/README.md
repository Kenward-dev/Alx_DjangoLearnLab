#Overview
    A simple Django blog application with user authentication, post management, and profile handling.

#Features
    User Authentication: Registration, login, and logout functionality.
    Post Management: Create, update, delete, and view blog posts.
    Profile Management: Update user profiles.
V#iews
    Create Post: Accessible to authenticated users only. Automatically sets the post author to the logged-in user.
    Update Post: Allows only the post author to edit their posts.
    Delete Post: Allows only the post author to delete their posts.
    List Posts: Displays all blog posts.
    Post Detail: Shows details for a specific post.
#URL Patterns
    / - List all posts
    /post/<int:pk>/ - Post detail
    /post/new/ - Create a new post
    /post/<int:pk>/edit/ - Edit an existing post
    /post/<int:pk>/delete/ - Delete a post
    /login/ - Login page
    /logout/ - Logout page
    /register/ - Registration page
    /profile/ - User profile page
#Authentication
    Uses LoginRequiredMixin to ensure users are logged in for creating posts.
    Uses UserPassesTestMixin to restrict editing and deletion to post authors.