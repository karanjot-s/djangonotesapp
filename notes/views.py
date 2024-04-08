from .serializers import UserSerializer, NoteSerializer
from .models import Note, SharedNote

from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from django.shortcuts import get_object_or_404


@api_view(["POST"])
def login(request):
    """
    Authenticate a user based on provided credentials and return an authentication token.

    This function attempts to authenticate a user by verifying the provided username
    and password against existing user records. If the credentials are valid, an
    authentication token is generated or retrieved for the user and returned along
    with serialized user details.

    Parameters:
        request (HttpRequest): The HTTP request object containing user credentials
            in the request data (username and password).

    Returns:
        Response: A JSON response containing the authentication token and user details.
            - If authentication is successful (HTTP 200 OK):
              {
                "token": "<authentication_token>",
                "user": {
                  "username": "<username>",
                  "email": "<email>"
                }
              }
            - If authentication fails due to invalid credentials (HTTP 400 Bad Request):
              {
                "message": "Invalid credentials"
              }
    """

    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(["POST"])
def signup(request):
    """
    Register a new user and generate an authentication token upon successful registration.

    Parameters:
        request (HttpRequest): The HTTP request object containing user registration data
            in the request data (username, email, password).

    Returns:
        Response: A JSON response containing an authentication token and user details upon
            successful registration.
            - If registration is successful (HTTP 201 Created):
              {
                "token": "<authentication_token>",
                "user": {
                  "id": <user_id>,
                  "username": "<username>",
                  "email": "<email>"
                }
              }
            - If registration fails due to invalid input (HTTP 400 Bad Request):
              {
                "errors": {
                  "field_name": ["error_message"]
                }
              }
    """

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=serializer.data["username"])
        user.set_password(request.data["password"])
        user.save()

        token = Token.objects.create(user=user)
        return Response(
            {"token": token.key, "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Log out the authenticated user by deleting their authentication token.

     Parameters:
        request (HttpRequest): The HTTP request object containing the user's authentication token.

    Returns:
        Response: A JSON response indicating the success or failure of the logout operation.
            - If logout is successful (HTTP 200 OK):
              {
                "message": "User logged out successfully"
              }
            - If an error occurs during logout (HTTP 500 Internal Server Error):
              {
                "error": "<error_message>"
              }

    Raises:
        None

    """

    try:
        request.user.auth_token.delete()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(
        {"message": "User logged out successfully"}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_note(request):
    """
    Create a new note for the authenticated user.

    Parameters:
        request (HttpRequest): The HTTP request object containing the data for the new note.

    Returns:
        Response: A JSON response indicating the success or failure of the note creation.
            - If note creation is successful (HTTP 201 Created):
              {
                "id": <note_id>,
                "title": "<note_title>",
                "content": "<note_content>",
                "timestamp": "<timestamp>"
              }
            - If there are validation errors in the input data (HTTP 400 Bad Request):
              {
                "errors": {
                  "field_name": ["error_message"]
                }
              }

    Raises:
        None
    """

    serializer = NoteSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def rud_note(request, pk):
    """
    Perform CRUD operations (Create, Retrieve, Update, Delete) on a specific note.

     Parameters:
        request (HttpRequest): The HTTP request object containing the data for CRUD operations.
        pk (int): The primary key (ID) of the note to perform operations on.

    Returns:
        Response: A JSON response indicating the result of the requested operation.
            - For GET request (Retrieve):
                - If the note is found (HTTP 200 OK):
                  {
                    "id": <note_id>,
                    "title": "<note_title>",
                    "content": "<note_content>",
                    "timestamp": "<timestamp>"
                  }
                - If the note is not found (HTTP 404 Not Found):
                  {
                    "error": "Note not found"
                  }
            - For POST request (Create):
                - If note creation is successful (HTTP 201 Created):
                  {
                    "id": <note_id>,
                    "title": "<note_title>",
                    "content": "<note_content>",
                    "timestamp": "<timestamp>"
                  }
                - If there are validation errors in the input data (HTTP 400 Bad Request):
                  {
                    "errors": {
                      "field_name": ["error_message"]
                    }
                  }
            - For PUT or PATCH request (Update):
                - If update is successful (HTTP 200 OK):
                  {
                    "id": <note_id>,
                    "title": "<updated_note_title>",
                    "content": "<updated_note_content>",
                    "timestamp": "<updated_timestamp>"
                  }
                - If there are validation errors or the note does not exist (HTTP 400 Bad Request or HTTP 404 Not Found):
                  {
                    "error": "Note not found"  # or validation error details
                  }
            - For DELETE request (Delete):
                - If deletion is successful (HTTP 204 No Content):
                  {
                    "message": "Note deleted successfully"
                  }
                - If the note does not exist (HTTP 404 Not Found):
                  {
                    "error": "Note not found"
                  }

    Raises:
        None
    """

    try:
        note = Note.objects.get(pk=pk, user=request.user)
    except Note.DoesNotExist:
        if request.method == "GET":
            try:
                shared_note = SharedNote.objects.get(note=pk, recipient=request.user)
                note = shared_note.note
            except SharedNote.DoesNotExist:
                return Response(
                    {"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND
            )

    serializer = NoteSerializer(note)

    if request.method == "GET":
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method in ["PUT", "PATCH"]:
        serializer = NoteSerializer(
            note, data=request.data, partial=request.method == "PATCH"
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        note.delete()
        return Response(
            {"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_created_notes(request):
    """
    Retrieve all notes created by the authenticated user with pagination.

    Parameters:
        request (HttpRequest): The HTTP request object used for retrieving notes.

    Returns:
        Response: A paginated JSON response containing notes created by the authenticated user.
            - If notes are found and pagination is successful (HTTP 200 OK):
              {
                "count": <total_notes_count>,
                "next": "<next_page_url>",
                "previous": "<previous_page_url>",
                "results": [
                  {
                    "id": <note_id>,
                    "title": "<note_title>",
                    "content": "<note_content>",
                    "timestamp": "<timestamp>"
                  },
                  ...
                ]
              }
            - If no notes are found (HTTP 200 OK):
              {
                "count": 0,
                "next": null,
                "previous": null,
                "results": []
              }

    Raises:
        None
    """

    paginator = PageNumberPagination()
    paginator.page_size = 10

    notes = Note.objects.filter(user=request.user).order_by("-timestamp")

    notes_paginated = paginator.paginate_queryset(notes, request)

    serializer = NoteSerializer(notes_paginated, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_shared_notes(request):
    """
    Retrieve all notes shared with the authenticated user with pagination.

    Parameters:
        request (HttpRequest): The HTTP request object used for retrieving shared notes.

    Returns:
        Response: A paginated JSON response containing notes shared with the authenticated user.
            - If shared notes are found and pagination is successful (HTTP 200 OK):
              {
                "count": <total_notes_count>,
                "next": "<next_page_url>",
                "previous": "<previous_page_url>",
                "results": [
                  {
                    "id": <note_id>,
                    "title": "<note_title>",
                    "content": "<note_content>",
                    "timestamp": "<timestamp>"
                  },
                  ...
                ]
              }
            - If no shared notes are found (HTTP 200 OK):
              {
                "count": 0,
                "next": null,
                "previous": null,
                "results": []
              }

    Raises:
        None
    """

    paginator = PageNumberPagination()
    paginator.page_size = 10  # Number of items per page

    # Retrieve notes associated with the authenticated user
    shared_notes = SharedNote.objects.filter(recipient=request.user).order_by(
        "-note__timestamp"
    )
    notes = [shared_note.note for shared_note in shared_notes]

    # Paginate the queryset
    notes_paginated = paginator.paginate_queryset(notes, request)

    # Serialize the paginated queryset
    serializer = NoteSerializer(notes_paginated, many=True)

    # Return paginated notes as a response
    return paginator.get_paginated_response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def share_note(request, pk):
    """
    Share a note with another user by specifying their email address.

    Parameters:
        request (HttpRequest): The HTTP request object used for sharing the note.
        pk (int): The primary key of the note to be shared.

    Request Body:
        {
          "email": "<recipient_email>"
        }

    Returns:
        Response: A JSON response indicating the result of the sharing operation.
            - If the note is successfully shared with the specified user (HTTP 200 OK):
              {
                "id": <note_id>,
                "title": "<note_title>",
                "content": "<note_content>",
                "timestamp": "<timestamp>"
              }
            - If the note is already shared with the specified user (HTTP 400 Bad Request):
              {
                "error": "Note is already shared with this user"
              }
            - If attempting to share a note with yourself (HTTP 400 Bad Request):
              {
                "error": "Cannot share note with yourself"
              }
            - If the specified note does not exist (HTTP 404 Not Found):
              {
                "error": "Note not found"
              }
            - If the recipient user specified by the email does not exist (HTTP 404 Not Found):
              {
                "error": "Recipient user not found"
              }

    Raises:
        None
    """

    try:
        note = Note.objects.get(pk=pk, user=request.user)
        serializer = NoteSerializer(note)

        recipient_email = request.data.get("email")
        recipient_user = User.objects.get(email=recipient_email)

        if note.user == recipient_user:
            return Response(
                {"error": "Cannot share note with yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if SharedNote.objects.filter(note=note, recipient=recipient_user).exists():
            return Response(
                {"error": "Note is already shared with this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        shared_note = SharedNote.objects.create(note=note, recipient=recipient_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Note.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response(
            {"error": "Recipient user not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
