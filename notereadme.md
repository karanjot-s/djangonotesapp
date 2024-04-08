# Notes API

## Table of contents

- [Create Note](#create-note)
- [Get Note by Id](#get-note-by-id)
- [Update Note by Id](#update-note-by-id)
- [Delete Note by Id](#delete-note-by-id)
- [Get All Notes created by the user](#get-all-notes-created-by-the-user)
- [Get All Notes shared to the user](#get-all-notes-shared-to-the-user)
- [Share a note to a user](#share-a-note-to-a-user)

## Create Note

Endpoint: `POST /api/note/`

- Example Usage:

  ```bash
    POST /api/note/
    Request Body:
    {
      "title": "Note Title",
      "content": "Note Content."
    }
    Headers:
    {
      "Authorization": "Token <authentication_token>"
    }
  ```

- Example Response (Success):

  ```bash
    HTTP 201 Created
    {
      "id": 1,
      "title": "Meeting Notes",
      "content": "Discuss project timelines and deliverables.",
      "timestamp": "2024-04-07T15:00:00Z"
    }
  ```

- Example Response (Error):
  ```bash
    HTTP 400 Bad Request
    {
      "errors": {
        "title": ["This field is required."],
        "content": ["Content must not be empty."]
      }
    }
  ```

## Get Note by Id

Endpoint: `GET /api/note/<pk>/`

- Example Usage:

  ```bash
    GET /api/note/1/
    Headers:
    {
      "Authorization": "Token <authentication_token>"
    }
  ```

- Example Response (Success):

  ```bash
    HTTP 200 OK
    {
      "id": 1,
      "title": "Meeting Notes",
      "content": "Discuss project timelines and deliverables.",
      "timestamp": "2024-04-07T15:00:00Z"
    }
  ```

- Example Response (Not Found):
  ```bash
    HTTP 404 Not Found
    {
      "error": "Note not found"
    }
  ```

## Update Note by Id

Endpoint: `PUT, PATCH /api/note/<pk>/`

- Example Usage:

  ```bash
    PUT /api/note/1/ or PATCH /api/note/1
    Request Body:
    {
      "title": "Note Title",
      "content": "Note Content."
    }
    Headers:
    {
      "Authorization": "Token <authentication_token>"
    }
  ```

- Example Response (Success):

  ```bash
    HTTP 200 OK
    {
      "id": 1,
      "title": "Meeting Notes",
      "content": "Discuss project timelines and deliverables.",
      "timestamp": "2024-04-07T15:00:00Z"
    }
  ```

- Example Response (Error):
  ```bash
    HTTP 400 Not Found
    {
      "errors": {...}
    }
  ```

## Delete Note by Id

Endpoint: `DELETE /api/note/<pk>/`

- Example Usage:

  ```bash
    DELETE /api/note/1/
    Headers:
    {
      "Authorization": "Token <authentication_token>"
    }
  ```

- Example Response (Success):

  ```bash
    HTTP 204 NO CONTENT
    {
      "message": "Note deleted successfully"
    }
  ```

- Example Response (Error):
  ```bash
    HTTP 500 SERVER ERROR
    {
      "errors": {...}
    }
  ```

## Get All Notes created by the user

Endpoint: `GET /api/notes/created/`

- Example Usage:

  ```bash
    GET /api/notes/created/
    Headers:
    {
      "Authorization": "Token <authentication_token>"
    }
  ```

- Example Response (Success):

  ```bash
    HTTP 200 OK
    {
      "count": 3,
      "next": "/api/notes/created/?page=2",
      "previous": null,
      "results": [
        {
          "id": 1,
          "title": "Meeting Notes",
          "content": "Discuss project timelines and deliverables.",
          "timestamp": "2024-04-07T15:00:00Z"
        },
        {
          "id": 2,
          "title": "Ideas for Proposal",
          "content": "Brainstorming session outcomes.",
          "timestamp": "2024-04-06T10:00:00Z"
        },
        {
          "id": 3,
          "title": "Task List",
          "content": "Complete tasks by end of the week.",
          "timestamp": "2024-04-05T14:30:00Z"
        }
      ]
    }
  ```

- Example Response (No note found):
  ```bash
    HTTP 200 OK
    {
      "count": 0,
      "next": null,
      "previous": null,
      "results": []
    }
  ```

## Get All Notes shared to the user

Endpoint: `GET /api/notes/shared/`

- Example Usage:

  ```bash
    GET /api/notes/shared/
    Headers:
    {
      "Authorization": "Token <authentication_token>"
    }
  ```

- Example Response (Success):

  ```bash
    HTTP 200 OK
    {
      "count": 3,
      "next": "/api/notes/shared/?page=2",
      "previous": null,
      "results": [
        {
          "id": 1,
          "title": "Meeting Notes",
          "content": "Discuss project timelines and deliverables.",
          "timestamp": "2024-04-07T15:00:00Z"
        },
        {
          "id": 2,
          "title": "Ideas for Proposal",
          "content": "Brainstorming session outcomes.",
          "timestamp": "2024-04-06T10:00:00Z"
        },
        {
          "id": 3,
          "title": "Task List",
          "content": "Complete tasks by end of the week.",
          "timestamp": "2024-04-05T14:30:00Z"
        }
      ]
    }
  ```

- Example Response (No note found):
  ```bash
    HTTP 200 OK
    {
      "count": 0,
      "next": null,
      "previous": null,
      "results": []
    }
  ```

## Share a note to a user

Endpoint: `GET /api/note/share/<int:pk>/`

- Example Usage:

  ```bash
    POST /api/note/share/1/
    Headers:
    {
      "Authorization": "Token <authentication_token>"
    }
    Request Body:
    {
      "email": "recipient@example.com"
    }
  ```

- Example Response (Success):

  ```bash
    HTTP 200 OK
    {
      "id": 1,
      "title": "Meeting Notes",
      "content": "Discuss project timelines and deliverables.",
      "timestamp": "2024-04-07T15:00:00Z"
    }
  ```

- Example Response (Note Already Shared):

  ```bash
    HTTP 400 Bad Request
    {
      "error": "Note is already shared with this user"
    }
  ```

- Example Response (Note Not Found):

  ```bash
    HTTP 404 Not Found
    {
      "error": "Note not found"
    }
  ```

- Example Response (Recipient User Not Found):
  ```bash
    HTTP 404 Not Found
    {
      "error": "Recipient user not found"
    }
  ```
