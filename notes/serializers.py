from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ["id", "username", "email", "password"]


class NoteSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Note
        fields = ["id", "title", "content", "timestamp"]
        read_only_fields = ["user"]
