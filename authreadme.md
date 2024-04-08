# User Authentication

## Table of Contents

- [Login](#login)
- [Signup](#signup)
- [Logout](#logout)

## Login

Endpoint: `POST /api/login/`

- Example Usage:

  ```bash
    POST /api/login/
    Request Body:
    {
      "username": "john_doe",
      "password": "securepassword"
    }
  ```

- Example Response (Success):

  ```bash
    HTTP 200 OK
    {
      "token": "<authentication_token>",
      "user": {
        "username": "john_doe",
        "email": "john@example.com"
      }
    }
  ```

- Example Response (Invalid Credentials):
  ```bash
    HTTP 400 Bad Request
    {
      "message": "Invalid credentials"
    }
  ```

## Signup

Endpoint: `POST /api/register/`

- Example Usage:

  ```bash
    POST /api/register/
    Request Body:
    {
      "username": "john_doe",
      "email": "john@example.com",
      "password": "securepassword"
    }
  ```

- Example Response (Success):

  ```bash
    HTTP 201 Created
    {
      "token": "<authentication_token>",
      "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
      }
    }
  ```

- Example Response (Validation Error):
  ```bash
    HTTP 400 Bad Request
    {
      "errors": {
        "username": ["This field must be unique."],
        "email": ["Enter a valid email address."],
        "password": ["Password must be at least 8 characters long."]
      }
    }
  ```

## Logout

Endpoint: `GET /api/logout/`

- Example Usage:

  ```bash
    GET /api/logout/
    Headers:
    {
      "Authorization": "Token <authentication_token>"
    }
  ```

- Example Response (Success):

  ```bash
    HTTP 200 OK
    {
      "message": "User logged out successfully"
    }
  ```

- Example Response (Error):
  ```bash
    HTTP 500 Internal Server Error
    {
      "error": "Token matching query does not exist."
    }
  ```
