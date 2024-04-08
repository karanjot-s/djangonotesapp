from django.urls import path
from . import views

urlpatterns = [
    path("register", views.signup, name="user_register"),
    path("login", views.login, name="user_login"),
    path("logout", views.logout, name="user_logout"),
    path("note/<int:pk>", views.rud_note, name="note_create"),
    path("note", views.create_note, name="note_create"),
    path("notes/created", views.get_all_created_notes, name="note_list"),
    path("notes/shared", views.get_all_shared_notes, name="note_list_shared"),
    path("note/share/<int:pk>", views.share_note, name="note_share"),
]
