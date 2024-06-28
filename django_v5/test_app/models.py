"""
Models for Django v5.0 test project app.
"""

# Third-Party Imports.
from django.contrib.auth.models import AbstractUser
from django.db import models
from localflavor.us.models import USStateField, USZipCodeField


MAX_LENGTH = 255


class BaseAbstractModel(models.Model):
    """Expanded version of the default Django model."""

    # Self-setting/Non-user-editable fields.
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class User(AbstractUser):
    """Custom user model definition.
    Defined as per the Django docs. Not yet directly used.
    """

    def clean(self, *args, **kwargs):
        """
        Custom cleaning implementation. Includes validation, setting fields, etc.
        """

    def save(self, *args, **kwargs):
        """
        Modify model save behavior.
        """
        # Check if new model.
        creating = False
        if self._state.adding:
            creating = True

        # Call parent logic.
        super().save(*args, **kwargs)

        # If new model, generate corresponding UserProfile object.
        if creating:
            UserProfile.objects.create(user=self)


class UserProfile(BaseAbstractModel):
    """Basic model to act as a test fk to user model."""

    # Relationship Keys.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Model Fields.
    address_1 = models.CharField(max_length=MAX_LENGTH, blank=True)
    address_2 = models.CharField(max_length=MAX_LENGTH, blank=True)
    city = models.CharField(max_length=MAX_LENGTH, blank=True)
    state = USStateField()
    zipcode = USZipCodeField()


class FavoriteFood(BaseAbstractModel):
    """Basic model to act as a test m2m relation to user model."""

    # Relationship Keys.
    user = models.ManyToManyField(User)

    # Model fields.
    name = models.CharField(max_length=MAX_LENGTH)


class ApiRequestJson(BaseAbstractModel):
    """Used to retain data for API testing views."""

    # Model fields.
    json_value = models.JSONField(default=dict)
