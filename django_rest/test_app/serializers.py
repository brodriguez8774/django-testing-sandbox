"""
Views for Django REST test project serializers.
"""

# System Imports.

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

# Internal Imports.


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'is_active',
            'is_superuser',
            'is_staff',
            'user_permissions',
            'groups',
            'last_login',
            'date_joined',
        ]


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for Django PermissionGroup model."""

    # Model Fields.
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Group
        fields = ['name', 'permissions']

