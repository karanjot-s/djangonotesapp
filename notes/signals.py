from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Note, SharedNote


@receiver(post_save, sender=Note)
def send_note_creation_notification(sender, instance, created, **kwargs):
    if created:
        print("Note created successfully by user:", instance.user.username)


@receiver(post_save, sender=SharedNote)
def send_note_sharing_notification(sender, instance, created, **kwargs):
    if created:
        print(
            "Note shared successfully by user:",
            instance.note.user.username,
            "with",
            instance.recipient.username,
        )
