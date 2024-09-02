# Book API

This project provides a set of API views to handle CRUD operations for the `Book` model using Django REST Framework. The `Book` model includes fields for `title`, `publication_year`, and a foreign key relationship to the `Author` model.

## Models

### Author
- **Fields:**
  - `name`: A string field to store the author's name.

### Book
- **Fields:**
  - `title`: A string field to store the title of the book.
  - `publication_year`: An integer field to store the year the book was published.
  - `author`: A foreign key linking to the `Author` model, establishing a one-to-many relationship from `Author` to `Books`.

## API Views

The following API views are implemented to manage `Book` instances:

### 1. ListView

- **URL**: `/api/books/`
- **Method**: `GET`
- **Description**: Retrieves a list of all books.
- **Permissions**: Read-only, accessible to all users, including unauthenticated users.

### 2. DetailView

- **URL**: `/api/books/<int:pk>/`
- **Method**: `GET`
- **Description**: Retrieves details of a single book by its ID.
- **Permissions**: Read-only, accessible to all users, including unauthenticated users.

### 3. CreateView

- **URL**: `/api/books/create/`
- **Method**: `POST`
- **Description**: Allows authenticated users to add a new book.
- **Permissions**: Restricted to authenticated users.

#### Custom Behavior:
The `create` method ensures that the submitted data is valid before saving the new book instance. If successful, the new book's data is returned in the response with a `201 Created` status.

### 4. UpdateView

- **URL**: `/api/books/update/<int:pk>/`
- **Method**: `PUT` or `PATCH`
- **Description**: Allows authenticated users to modify an existing book.
- **Permissions**: Restricted to authenticated users.

#### Custom Behavior:
The `update` method ensures that only valid data is processed when updating a book. Partial updates are supported with the `PATCH` method.

### 5. DeleteView

- **URL**: `/api/books/delete/<int:pk>/`
- **Method**: `DELETE`
- **Description**: Allows authenticated users to remove a book.
- **Permissions**: Restricted to authenticated users.

## Permissions

- **Authenticated users**: Can create, update, and delete books.
- **Unauthenticated users**: Can only view book details and list of books.

## Usage

To use the API views, make sure you have the Django project running. You can interact with the API using tools like Postman, cURL, or any other API client.
