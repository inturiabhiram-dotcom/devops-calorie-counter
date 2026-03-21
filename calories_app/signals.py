"""Signals for calories_app."""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from calories_app.models import Profile

def create_profile(sender, instance, created, **kwargs):
    """Create a Profile automatically when a User is created."""
    _ = sender
    _ = kwargs

    if created:
        Profile.objects.create(person_of=instance)
        print("profile created")


post_save.connect(create_profile, sender=User)
