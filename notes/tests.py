from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Note, SharedNote
from rest_framework.authtoken.models import Token
from .serializers import NoteSerializer


class APITests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )

        self.token = Token.objects.create(user=self.user)

        # Create a test note
        self.note = Note.objects.create(
            user=self.user, title="Test Note", content="This is a test note"
        )

        # Create an API client
        self.client = APIClient()

        # Authenticate the client with the test user
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        # Clean up test data
        self.user.delete()
        self.note.delete()

    def test_user_login(self):
        # Test user login
        url = reverse("user_login")
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("user", response.data)

    def test_user_register(self):
        # Test user registration
        url = reverse("user_register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertIn("user", response.data)

    def test_create_note(self):
        # Test creating a new note
        url = reverse("note_create")
        data = {"title": "New Note", "content": "This is a new note"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_created_notes(self):
        # Test retrieving all created notes
        url = reverse("note_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_share_note(self):
        # Test sharing a note with another user
        recipient_user = User.objects.create_user(
            username="recipient", email="recipient@example.com", password="password456"
        )
        url = reverse("note_share", kwargs={"pk": self.note.id})
        data = {"email": "recipient@example.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            SharedNote.objects.filter(note=self.note, recipient=recipient_user).exists()
        )

    def test_get_all_shared_notes(self):
        # Test retrieving all shared notes for the user
        url = reverse("note_list_shared")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        # Test user logout
        url = reverse("user_logout")
        response = self.client.get(url)  # Send POST request to logout endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)
