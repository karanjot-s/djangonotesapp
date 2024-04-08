# Django Notes App

This Django application implements a RESTful API for managing notes with user authentication and sharing capabilities.

## Table of Contents

- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Authentication and Authorization](#authentication-and-authorization)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Installation

Follow these steps to set up and run the Django Notes App locally:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/django-notes-app.git
   cd django-notes-app
   ```

2. **Set Up a Virtual Environment:**

   ```bash
    python -m venv venv
    source venv/bin/activate  # Activate the virtual environment (Linux/macOS)
    # or
    .\venv\Scripts\activate  # Activate the virtual environment (Windows)
   ```

3. **Install Dependencies:**

   ```bash
    pip install -r requirements.txt
   ```

4. **Apply Database Migrations:**

   ```bash
    python manage.py migrate
   ```

5. **Run the Development Server:**

   ```bash
    python manage.py runserver
   ```

6. **Access the API:**

   Open your web browser or use API testing tools like Postman to interact with the API at http://127.0.0.1:8000/api/.

## API Endpoints

- ### User Authentication:

  - `POST /api/register/`: Register a new user.
  - `POST /api/login/`: Log in and obtain an authentication token.
  - `POST /api/logout/`: Log out and invalidate the authentication token.

  [View more about Authentication API](authreadme.md)

- ### Notes Management:

  - `POST /api/note/`: Create a new note.
  - `GET /api/note/<note_id>/`: Retrieve a specific note.
  - `PUT /api/note/<note_id>/`: Update a note.
  - `DELETE /api/note/<note_id>/`: Delete a note.

  [View more about Notes API](notereadme.md)

- ### Note Sharing:

  - `POST /api/note/share/<note_id>/`: Share a note with another user by specifying their email address.
  - `GET /api/notes/created/`: Get all notes created by the authenticated user.
  - `GET /api/notes/shared/`: Get all notes shared with the authenticated user.

  [View more about Notes API](notereadme.md)

## Authentication and Authorization

- Authentication is based on token authentication using djangorestframework.authtoken.
- Users must include their authentication token in the Authorization header for authenticated endpoints.

# Technologies Used

- Django
- Django Rest Framework (DRF)
- SQLite3 (or your preferred database)
- Python 3.10.0

# Contributing

Contributions to this project are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
