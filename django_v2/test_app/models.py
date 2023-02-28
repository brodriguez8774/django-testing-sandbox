"""
Models for Django v2.2 test project app.
"""

# Third-Party Imports.
from django.contrib.auth.models import AbstractUser
from django.db import models
from localflavor.us.models import USStateField, USZipCodeField


MAX_LENGTH = 255


class User(AbstractUser):
    """Custom user model definition.
    Defined as per the Django docs. Not yet directly used.
    """
    pass


class UserProfile(models.Model):
    """Basic model to act as a test fk to user model."""

    # Relationship Keys.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Model Fields.
    address_1 = models.CharField(max_length=MAX_LENGTH, blank=True)
    address_2 = models.CharField(max_length=MAX_LENGTH, blank=True)
    city = models.CharField(max_length=MAX_LENGTH, blank=True)
    state = USStateField()
    zipcode = USZipCodeField()


class FavoriteFood(models.Model):
    """Basic model to act as a test m2m relation to user model."""

    # Relationship Keys.
    user = models.ManyToManyField(User)

    # Model fields.
    name = models.CharField(max_length=MAX_LENGTH)
